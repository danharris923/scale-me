"""
File generation tool for creating React/Next.js affiliate marketing websites.

This module generates complete file structures with proper TypeScript,
Next.js routing, and conversion-optimized components.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

from .template_generator import TemplateGenerator
from agents.models import GeneratedWebsite, WebsiteGenerationRequest, SEOOptimization

logger = logging.getLogger(__name__)


class FileGenerator:
    """Generates complete website file structures."""
    
    def __init__(self, template_directory: str = "./templates", output_directory: str = "./generated"):
        self.template_dir = Path(template_directory)
        self.output_dir = Path(output_directory)
        self.template_generator = TemplateGenerator(template_directory)
    
    async def generate_website(self, request: WebsiteGenerationRequest) -> GeneratedWebsite:
        """Generate complete website structure."""
        try:
            project_name = request.brand_name.lower().replace(' ', '-')
            project_path = self.output_dir / project_name
            
            # Create project directory
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Generate file structure
            file_structure = {}
            
            # Core Next.js files
            file_structure.update(await self._generate_nextjs_files(request, project_path))
            
            # React components
            file_structure.update(await self._generate_components(request, project_path))
            
            # Configuration files
            file_structure.update(await self._generate_config_files(request, project_path))
            
            # Package.json
            package_json = await self._generate_package_json(request)
            self._write_file(project_path / "package.json", json.dumps(package_json, indent=2))
            file_structure["package.json"] = json.dumps(package_json, indent=2)
            
            # Vercel config
            vercel_config = await self._generate_vercel_config(request)
            self._write_file(project_path / "vercel.json", json.dumps(vercel_config, indent=2))
            file_structure["vercel.json"] = json.dumps(vercel_config, indent=2)
            
            return GeneratedWebsite(
                project_name=project_name,
                file_structure=file_structure,
                package_json=package_json,
                vercel_config=vercel_config,
                environment_variables=self._get_env_vars(request)
            )
            
        except Exception as e:
            logger.error(f"Website generation failed: {e}")
            raise
    
    async def _generate_nextjs_files(self, request: WebsiteGenerationRequest, project_path: Path) -> Dict[str, str]:
        """Generate Next.js page files."""
        files = {}
        pages_dir = project_path / "pages"
        pages_dir.mkdir(exist_ok=True)
        
        # Index page
        index_content = self.template_generator.generate_page(
            "index",
            {
                "brand_name": request.brand_name,
                "niche": request.niche.value,
                "target_audience": request.target_audience,
                "sheets_config": request.sheets_config.dict()
            }
        )
        self._write_file(pages_dir / "index.tsx", index_content)
        files["pages/index.tsx"] = index_content
        
        # Category pages
        category_dir = pages_dir / "category"
        category_dir.mkdir(exist_ok=True)
        
        category_content = self.template_generator.generate_page(
            "category/[slug]",
            {
                "brand_name": request.brand_name,
                "niche": request.niche.value,
                "sheets_config": request.sheets_config.dict()
            }
        )
        self._write_file(category_dir / "[slug].tsx", category_content)
        files["pages/category/[slug].tsx"] = category_content
        
        # API routes
        api_dir = pages_dir / "api"
        api_dir.mkdir(exist_ok=True)
        
        sheets_api = self.template_generator.generate_api_route(
            "sheets",
            {"sheets_config": request.sheets_config.dict()}
        )
        self._write_file(api_dir / "sheets.ts", sheets_api)
        files["pages/api/sheets.ts"] = sheets_api
        
        return files
    
    async def _generate_components(self, request: WebsiteGenerationRequest, project_path: Path) -> Dict[str, str]:
        """Generate React components."""
        files = {}
        components_dir = project_path / "components"
        components_dir.mkdir(exist_ok=True)
        
        # Product Card component
        product_card = self.template_generator.generate_component(
            "ProductCard",
            "ProductCard",
            {"product": "Product", "onAddToCart": "() => void"},
            "conversion-optimized",
            niche=request.niche
        )
        self._write_file(components_dir / "ProductCard.tsx", product_card)
        files["components/ProductCard.tsx"] = product_card
        
        # Hero component
        hero = self.template_generator.generate_component(
            "Hero",
            "Hero",
            {"brandName": "string", "tagline": "string"},
            "conversion-optimized",
            niche=request.niche
        )
        self._write_file(components_dir / "Hero.tsx", hero)
        files["components/Hero.tsx"] = hero
        
        # Navigation component
        nav = self.template_generator.generate_component(
            "Navigation",
            "Navigation",
            {"brandName": "string", "categories": "string[]"},
            "mobile-first",
            niche=request.niche
        )
        self._write_file(components_dir / "Navigation.tsx", nav)
        files["components/Navigation.tsx"] = nav
        
        # Footer component
        footer = self.template_generator.generate_component(
            "Footer",
            "Footer",
            {"brandName": "string", "description": "string"},
            "conversion-optimized",
            niche=request.niche
        )
        self._write_file(components_dir / "Footer.tsx", footer)
        files["components/Footer.tsx"] = footer
        
        return files
    
    async def _generate_config_files(self, request: WebsiteGenerationRequest, project_path: Path) -> Dict[str, str]:
        """Generate configuration files."""
        files = {}
        
        # Tailwind config
        tailwind_config = self.template_generator.generate_config_file(
            "tailwind.config.js",
            {
                "brand_name": request.brand_name,
                "niche": request.niche.value,
                "color_scheme": request.color_scheme
            }
        )
        self._write_file(project_path / "tailwind.config.js", tailwind_config)
        files["tailwind.config.js"] = tailwind_config
        
        # Next.js config
        next_config = '''/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['images.unsplash.com', 'via.placeholder.com'],
    formats: ['image/webp', 'image/avif'],
  },
  experimental: {
    optimizeCss: true,
  },
}

module.exports = nextConfig'''
        
        self._write_file(project_path / "next.config.js", next_config)
        files["next.config.js"] = next_config
        
        return files
    
    async def _generate_package_json(self, request: WebsiteGenerationRequest) -> Dict[str, Any]:
        """Generate package.json content."""
        return {
            "name": request.brand_name.lower().replace(' ', '-'),
            "version": "1.0.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint"
            },
            "dependencies": {
                "next": "^14.0.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "typescript": "^5.2.0",
                "@types/node": "^20.8.0",
                "@types/react": "^18.2.0",
                "@types/react-dom": "^18.2.0",
                "tailwindcss": "^3.3.0",
                "autoprefixer": "^10.4.0",
                "postcss": "^8.4.0",
                "googleapis": "^128.0.0"
            },
            "devDependencies": {
                "eslint": "^8.51.0",
                "eslint-config-next": "^14.0.0"
            }
        }
    
    async def _generate_vercel_config(self, request: WebsiteGenerationRequest) -> Dict[str, Any]:
        """Generate Vercel configuration."""
        return {
            "version": 2,
            "build": {
                "env": {
                    "NODE_ENV": "production"
                }
            },
            "functions": {
                "pages/api/sheets.ts": {
                    "runtime": "nodejs18.x"
                }
            }
        }
    
    def _get_env_vars(self, request: WebsiteGenerationRequest) -> Dict[str, str]:
        """Get environment variables for the project."""
        return {
            "GOOGLE_SHEETS_API_KEY": "your-google-sheets-api-key",
            "NEXT_PUBLIC_BRAND_NAME": request.brand_name,
            "NEXT_PUBLIC_NICHE": request.niche.value
        }
    
    def _write_file(self, path: Path, content: str) -> None:
        """Write content to file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        logger.debug(f"Generated file: {path}")
    
    def validate_generated_files(self, project_path: Path) -> Dict[str, bool]:
        """Validate generated files for syntax and completeness."""
        validation_results = {}
        
        # Check TypeScript files
        for ts_file in project_path.rglob("*.tsx"):
            try:
                content = ts_file.read_text()
                is_valid = self.template_generator.validate_typescript(content)
                validation_results[str(ts_file.relative_to(project_path))] = is_valid
            except Exception as e:
                logger.warning(f"Validation error for {ts_file}: {e}")
                validation_results[str(ts_file.relative_to(project_path))] = False
        
        return validation_results