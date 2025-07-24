"""
Google Sheets integration tool for fetching product data.

This module provides secure authentication (OAuth2/Service Account),
real-time data fetching with caching, and robust error handling
for Google Sheets API integration.
"""

import os
import json
import asyncio
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
from pathlib import Path
import logging

from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import httpx

from agents.models import ProductSchema, GoogleSheetsConfig
from config import Settings

logger = logging.getLogger(__name__)


class SheetsIntegrationError(Exception):
    """Custom exception for Google Sheets integration errors."""
    pass


class SheetsCache:
    """Simple in-memory cache for Google Sheets data."""
    
    def __init__(self, default_ttl: int = 300):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached data if not expired."""
        if key not in self._cache:
            return None
        
        data = self._cache[key]
        if datetime.now() > data['expires_at']:
            del self._cache[key]
            return None
        
        return data['value']
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cached data with expiration."""
        ttl = ttl or self.default_ttl
        self._cache[key] = {
            'value': value,
            'expires_at': datetime.now() + timedelta(seconds=ttl)
        }
    
    def clear(self, pattern: Optional[str] = None) -> None:
        """Clear cache entries matching pattern."""
        if pattern:
            keys_to_delete = [k for k in self._cache.keys() if pattern in k]
            for key in keys_to_delete:
                del self._cache[key]
        else:
            self._cache.clear()


class SheetsIntegrationTool:
    """Google Sheets integration tool with authentication and caching."""
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.cache = SheetsCache(default_ttl=self.settings.cache_ttl)
        self._service = None
        self._credentials = None
    
    async def authenticate(self, config: GoogleSheetsConfig) -> None:
        """Authenticate with Google Sheets API."""
        try:
            if config.service_account_path and os.path.exists(config.service_account_path):
                # Use Service Account authentication
                await self._authenticate_service_account(config.service_account_path)
            elif config.api_key:
                # Use API key for public sheets (limited functionality)
                self._credentials = None  # API key doesn't use credentials
            elif self.settings.google_sheets_service_account:
                # Use service account from environment
                await self._authenticate_service_account_from_env()
            else:
                raise SheetsIntegrationError(
                    "No valid authentication method provided. "
                    "Please provide either service_account_path or api_key."
                )
            
            logger.info("Successfully authenticated with Google Sheets API")
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise SheetsIntegrationError(f"Authentication failed: {e}")
    
    async def _authenticate_service_account(self, service_account_path: str) -> None:
        """Authenticate using service account JSON file."""
        try:
            self._credentials = service_account.Credentials.from_service_account_file(
                service_account_path, scopes=self.SCOPES
            )
            self._service = build('sheets', 'v4', credentials=self._credentials)
        except Exception as e:
            raise SheetsIntegrationError(f"Service account authentication failed: {e}")
    
    async def _authenticate_service_account_from_env(self) -> None:
        """Authenticate using service account from environment variable."""
        try:
            service_account_info = json.loads(self.settings.google_sheets_service_account)
            self._credentials = service_account.Credentials.from_service_account_info(
                service_account_info, scopes=self.SCOPES
            )
            self._service = build('sheets', 'v4', credentials=self._credentials)
        except Exception as e:
            raise SheetsIntegrationError(f"Environment service account authentication failed: {e}")
    
    async def fetch_sheet_data(
        self, 
        config: GoogleSheetsConfig,
        category_filter: Optional[str] = None
    ) -> List[ProductSchema]:
        """Fetch and validate product data from Google Sheets."""
        # Generate cache key
        cache_key = f"{config.sheet_id}-{config.range_name}-{category_filter or 'all'}"
        
        # Check cache first
        cached_data = self.cache.get(cache_key)
        if cached_data:
            logger.info(f"Returning cached data for {cache_key}")
            return [ProductSchema(**product) for product in cached_data]
        
        try:
            # Authenticate if not already done
            if not self._service and not config.api_key:
                await self.authenticate(config)
            
            # Fetch raw data
            raw_data = await self._fetch_raw_data(config)
            
            # Validate and transform data
            products = await self._validate_and_transform_data(raw_data, category_filter)
            
            # Cache the results
            product_dicts = [product.dict() for product in products]
            self.cache.set(cache_key, product_dicts, config.cache_duration)
            
            logger.info(f"Fetched and cached {len(products)} products from Google Sheets")
            return products
            
        except Exception as e:
            logger.error(f"Error fetching sheet data: {e}")
            raise SheetsIntegrationError(f"Failed to fetch sheet data: {e}")
    
    async def _fetch_raw_data(self, config: GoogleSheetsConfig) -> List[List[Any]]:
        """Fetch raw data from Google Sheets."""
        try:
            if config.api_key:
                # Use API key for public sheets
                return await self._fetch_with_api_key(config)
            else:
                # Use service account
                return await self._fetch_with_service_account(config)
        except HttpError as e:
            if e.resp.status == 403:
                raise SheetsIntegrationError("Permission denied. Check sheet permissions and credentials.")
            elif e.resp.status == 404:
                raise SheetsIntegrationError("Spreadsheet not found. Check the sheet ID.")
            else:
                raise SheetsIntegrationError(f"Google Sheets API error: {e}")
    
    async def _fetch_with_api_key(self, config: GoogleSheetsConfig) -> List[List[Any]]:
        """Fetch data using API key (for public sheets)."""
        url = (
            f"https://sheets.googleapis.com/v4/spreadsheets/{config.sheet_id}/values/{config.range_name}"
            f"?key={config.api_key}"
        )
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            data = response.json()
            return data.get('values', [])
    
    async def _fetch_with_service_account(self, config: GoogleSheetsConfig) -> List[List[Any]]:
        """Fetch data using service account credentials."""
        if not self._service:
            raise SheetsIntegrationError("Service not initialized. Call authenticate() first.")
        
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        
        def _fetch():
            result = self._service.spreadsheets().values().get(
                spreadsheetId=config.sheet_id,
                range=config.range_name,
                majorDimension='ROWS',
                valueRenderOption='UNFORMATTED_VALUE',
                dateTimeRenderOption='FORMATTED_STRING'
            ).execute()
            return result.get('values', [])
        
        return await loop.run_in_executor(None, _fetch)
    
    async def _validate_and_transform_data(
        self, 
        raw_data: List[List[Any]], 
        category_filter: Optional[str] = None
    ) -> List[ProductSchema]:
        """Validate and transform raw sheet data into ProductSchema objects."""
        products = []
        
        for i, row in enumerate(raw_data):
            # Skip header row
            if i == 0:
                continue
            
            try:
                # Ensure we have enough columns
                while len(row) < 10:
                    row.append('')
                
                # Extract and validate data
                product_data = {
                    'id': str(row[0]).strip() if row[0] else f'product-{i}',
                    'name': str(row[1]).strip() if row[1] else 'Unnamed Product',
                    'price': float(row[2]) if row[2] and str(row[2]).replace('.', '').isdigit() else 0,
                    'image_url': str(row[3]).strip() if row[3] else 'https://via.placeholder.com/400x400',
                    'affiliate_url': str(row[4]).strip() if row[4] else '#',
                    'category': str(row[5]).strip() if row[5] else 'Uncategorized',
                    'description': str(row[6]).strip() if row[6] else None,
                    'discount_percent': float(row[7]) if row[7] and str(row[7]).replace('.', '').isdigit() else None,
                    'is_featured': self._parse_boolean(row[8]),
                    'stock_status': self._parse_stock_status(row[9])
                }
                
                # Apply category filter
                if category_filter and product_data['category'].lower() != category_filter.lower():
                    continue
                
                # Validate URLs
                if not self._is_valid_url(product_data['image_url']):
                    product_data['image_url'] = 'https://via.placeholder.com/400x400'
                
                if not self._is_valid_url(product_data['affiliate_url']):
                    logger.warning(f"Invalid affiliate URL in row {i+1}: {product_data['affiliate_url']}")
                    continue
                
                # Skip if price is invalid
                if product_data['price'] <= 0:
                    logger.warning(f"Invalid price in row {i+1}: {product_data['price']}")
                    continue
                
                # Create and validate ProductSchema
                product = ProductSchema(**product_data)
                products.append(product)
                
            except Exception as e:
                logger.warning(f"Error processing row {i+1}: {e}")
                continue
        
        return products
    
    def _parse_boolean(self, value: Any) -> bool:
        """Parse boolean value from sheet cell."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        if isinstance(value, (int, float)):
            return bool(value)
        return False
    
    def _parse_stock_status(self, value: Any) -> str:
        """Parse stock status from sheet cell."""
        if not value:
            return 'in_stock'
        
        status = str(value).lower().strip()
        if status in ['out_of_stock', 'out of stock', 'unavailable']:
            return 'out_of_stock'
        elif status in ['low_stock', 'low stock', 'limited']:
            return 'low_stock'
        else:
            return 'in_stock'
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid."""
        if not url or not isinstance(url, str):
            return False
        return url.startswith(('http://', 'https://'))
    
    async def test_connection(self, config: GoogleSheetsConfig) -> Dict[str, Any]:
        """Test connection to Google Sheets."""
        try:
            await self.authenticate(config)
            
            # Try to fetch just the first row for testing
            test_config = GoogleSheetsConfig(
                sheet_id=config.sheet_id,
                range_name=f"{config.range_name.split('!')[0]}!A1:J1",
                api_key=config.api_key,
                service_account_path=config.service_account_path
            )
            
            raw_data = await self._fetch_raw_data(test_config)
            
            return {
                'success': True,
                'message': 'Connection successful',
                'headers': raw_data[0] if raw_data else [],
                'sheet_id': config.sheet_id,
                'range': config.range_name
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Connection failed: {e}',
                'sheet_id': config.sheet_id,
                'range': config.range_name
            }
    
    async def generate_integration_code(
        self, 
        config: GoogleSheetsConfig, 
        output_format: str = "nextjs_api_route"
    ) -> str:
        """Generate integration code for different frameworks."""
        if output_format == "nextjs_api_route":
            return self._generate_nextjs_api_route(config)
        elif output_format == "react_hook":
            return self._generate_react_hook(config)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def _generate_nextjs_api_route(self, config: GoogleSheetsConfig) -> str:
        """Generate Next.js API route code."""
        # This would typically use a template, but for now return basic structure
        return f"""
// Generated Google Sheets API route
import {{ NextApiRequest, NextApiResponse }} from 'next';
import {{ SheetsIntegrationTool }} from '../../../tools/sheets_integration';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {{
  if (req.method !== 'GET') {{
    return res.status(405).json({{ error: 'Method not allowed' }});
  }}

  try {{
    const tool = new SheetsIntegrationTool();
    const config = {{
      sheet_id: '{config.sheet_id}',
      range_name: '{config.range_name}',
      api_key: process.env.GOOGLE_SHEETS_API_KEY,
      cache_duration: {config.cache_duration}
    }};

    const products = await tool.fetch_sheet_data(config, req.query.category);
    
    res.setHeader('Cache-Control', 'public, s-maxage=300, stale-while-revalidate=600');
    return res.status(200).json({{ products, timestamp: Date.now() }});
    
  }} catch (error) {{
    console.error('Sheets API error:', error);
    return res.status(500).json({{ error: 'Failed to fetch data' }});
  }}
}}
"""
    
    def _generate_react_hook(self, config: GoogleSheetsConfig) -> str:
        """Generate React hook code."""
        return f"""
// Generated React hook for Google Sheets data
import {{ useState, useEffect }} from 'react';

interface Product {{
  id: string;
  name: string;
  price: number;
  // ... other fields
}}

export const useGoogleSheets = (category?: string) => {{
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {{
    const fetchProducts = async () => {{
      try {{
        setLoading(true);
        const params = new URLSearchParams({{
          sheetId: '{config.sheet_id}',
          range: '{config.range_name}',
          ...(category && {{ category }})
        }});

        const response = await fetch(`/api/sheets?${{params}}`);
        const data = await response.json();

        if (data.error) {{
          throw new Error(data.error);
        }}

        setProducts(data.products);
      }} catch (err) {{
        setError(err instanceof Error ? err.message : 'Unknown error');
      }} finally {{
        setLoading(false);
      }}
    }};

    fetchProducts();
  }}, [category]);

  return {{ products, loading, error }};
}};
"""
    
    def clear_cache(self, sheet_id: Optional[str] = None) -> None:
        """Clear cache entries."""
        if sheet_id:
            self.cache.clear(sheet_id)
        else:
            self.cache.clear()