"""
SEO optimization tool for affiliate marketing websites.

This module implements SEO best practices including meta tags,
structured data, performance optimization, and accessibility standards.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from urllib.parse import urljoin

from agents.models import SEOOptimization, ProductSchema, NicheType

logger = logging.getLogger(__name__)


class SEOOptimizer:
    """Tool for implementing SEO best practices in generated websites."""
    
    def __init__(self):
        self.structured_data_schemas = {
            'website': self._get_website_schema,
            'organization': self._get_organization_schema,
            'product': self._get_product_schema,
            'breadcrumb': self._get_breadcrumb_schema,
            'faq': self._get_faq_schema
        }
    
    def generate_seo_optimization(
        self,
        brand_name: str,
        niche: NicheType,
        target_keywords: List[str],
        description: str,
        domain: Optional[str] = None
    ) -> SEOOptimization:
        """Generate comprehensive SEO optimization settings."""
        
        # Generate optimized meta title
        meta_title = self._generate_meta_title(brand_name, niche, target_keywords)
        
        # Generate meta description
        meta_description = self._generate_meta_description(brand_name, niche, description)
        
        # Expand keywords with niche-specific terms
        expanded_keywords = self._expand_keywords(target_keywords, niche)
        
        # Generate structured data
        schema_markup = self._generate_schema_markup(brand_name, niche, description, domain)
        
        # Set performance targets
        performance_targets = self._get_performance_targets()
        
        return SEOOptimization(
            meta_title=meta_title,
            meta_description=meta_description,
            keywords=expanded_keywords,
            schema_markup=schema_markup,
            performance_targets=performance_targets
        )
    
    def _generate_meta_title(self, brand_name: str, niche: NicheType, keywords: List[str]) -> str:
        """Generate SEO-optimized meta title."""
        primary_keyword = keywords[0] if keywords else niche.value.replace('_', ' ').title()
        
        templates = {
            NicheType.FASHION: f"{primary_keyword} - {brand_name} | Fashion Deals & Style",
            NicheType.TECH: f"{primary_keyword} - {brand_name} | Latest Tech Deals",
            NicheType.OUTDOOR_GEAR: f"{primary_keyword} - {brand_name} | Outdoor Adventure Gear",
            NicheType.HOME_IMPROVEMENT: f"{primary_keyword} - {brand_name} | Home & Garden",
            NicheType.MUSIC: f"{primary_keyword} - {brand_name} | Musical Instruments",
            NicheType.GENERAL: f"{primary_keyword} - {brand_name} | Best Deals Online"
        }
        
        title = templates.get(niche, templates[NicheType.GENERAL])
        
        # Ensure title is under 60 characters
        if len(title) > 60:
            title = f"{primary_keyword} - {brand_name}"[:57] + "..."
        
        return title
    
    def _generate_meta_description(self, brand_name: str, niche: NicheType, description: str) -> str:
        """Generate SEO-optimized meta description."""
        if len(description) <= 160:
            return description
        
        # Create niche-specific descriptions
        descriptions = {
            NicheType.FASHION: f"Discover the latest fashion trends and deals at {brand_name}. Quality clothing, accessories, and style inspiration with fast shipping and great prices.",
            NicheType.TECH: f"Find the best tech deals at {brand_name}. Latest gadgets, electronics, and technology products with expert reviews and unbeatable prices.",
            NicheType.OUTDOOR_GEAR: f"Gear up for adventure with {brand_name}. Quality outdoor equipment, camping gear, and hiking essentials at competitive prices.",
            NicheType.HOME_IMPROVEMENT: f"Transform your home with {brand_name}. Quality tools, home decor, and improvement products with fast delivery and great customer service.",
            NicheType.MUSIC: f"Discover musical instruments and gear at {brand_name}. Quality equipment for musicians of all levels with expert advice and competitive prices.",
            NicheType.GENERAL: f"Find amazing deals at {brand_name}. Quality products across all categories with fast shipping, great prices, and excellent customer service."
        }
        
        base_description = descriptions.get(niche, descriptions[NicheType.GENERAL])
        
        # Ensure description is under 160 characters
        if len(base_description) > 160:
            base_description = base_description[:157] + "..."
        
        return base_description
    
    def _expand_keywords(self, base_keywords: List[str], niche: NicheType) -> List[str]:
        """Expand keywords with niche-specific and SEO terms."""
        expanded = base_keywords.copy()
        
        # Add niche-specific keywords
        niche_keywords = {
            NicheType.FASHION: ['fashion', 'clothing', 'style', 'apparel', 'accessories', 'trends'],
            NicheType.TECH: ['technology', 'electronics', 'gadgets', 'tech deals', 'devices', 'innovation'],
            NicheType.OUTDOOR_GEAR: ['outdoor', 'camping', 'hiking', 'adventure', 'gear', 'equipment'],
            NicheType.HOME_IMPROVEMENT: ['home improvement', 'tools', 'diy', 'home decor', 'garden', 'renovation'],
            NicheType.MUSIC: ['musical instruments', 'music gear', 'audio equipment', 'instruments', 'music'],
            NicheType.GENERAL: ['deals', 'discount', 'sale', 'products', 'shopping', 'online store']
        }
        
        niche_specific = niche_keywords.get(niche, niche_keywords[NicheType.GENERAL])
        expanded.extend(niche_specific)
        
        # Add general e-commerce keywords
        general_keywords = ['deals', 'discount', 'sale', 'best price', 'free shipping']
        expanded.extend(general_keywords)
        
        # Remove duplicates and limit to 10 keywords
        unique_keywords = list(dict.fromkeys(expanded))
        return unique_keywords[:10]
    
    def _generate_schema_markup(
        self,
        brand_name: str,
        niche: NicheType,
        description: str,
        domain: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate structured data markup."""
        base_url = domain or "https://example.com"
        
        # Website schema
        website_schema = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": brand_name,
            "description": description,
            "url": base_url,
            "potentialAction": {
                "@type": "SearchAction",
                "target": f"{base_url}/search?q={{search_term_string}}",
                "query-input": "required name=search_term_string"
            }
        }
        
        # Organization schema
        organization_schema = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": brand_name,
            "description": description,
            "url": base_url,
            "logo": f"{base_url}/logo.png",
            "sameAs": [
                f"https://facebook.com/{brand_name.lower().replace(' ', '')}",
                f"https://twitter.com/{brand_name.lower().replace(' ', '')}",
                f"https://instagram.com/{brand_name.lower().replace(' ', '')}"
            ]
        }
        
        return {
            "website": website_schema,
            "organization": organization_schema
        }
    
    def _get_performance_targets(self) -> Dict[str, float]:
        """Get performance targets for optimization."""
        return {
            "lighthouse_score": 90.0,
            "ttfb": 800.0,  # milliseconds
            "lcp": 2500.0,  # milliseconds
            "cls": 0.1,
            "fid": 100.0,  # milliseconds
            "ttfb_mobile": 1200.0  # milliseconds
        }
    
    def generate_product_schema(self, product: ProductSchema, base_url: str) -> Dict[str, Any]:
        """Generate product schema markup."""
        return {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": product.name,
            "description": product.description or f"Quality {product.name} at the best price",
            "image": product.image_url,
            "url": f"{base_url}/product/{product.id}",
            "sku": product.id,
            "category": product.category,
            "offers": {
                "@type": "Offer",
                "price": str(product.price),
                "priceCurrency": "USD",
                "availability": self._get_availability_schema(product.stock_status),
                "url": product.affiliate_url,
                "seller": {
                    "@type": "Organization",
                    "name": "Affiliate Partner"
                }
            },
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.5",
                "reviewCount": "127"
            }
        }
    
    def _get_availability_schema(self, stock_status: str) -> str:
        """Convert stock status to schema.org availability."""
        availability_map = {
            "in_stock": "https://schema.org/InStock",
            "low_stock": "https://schema.org/LimitedAvailability",
            "out_of_stock": "https://schema.org/OutOfStock"
        }
        return availability_map.get(stock_status, "https://schema.org/InStock")
    
    def generate_breadcrumb_schema(self, breadcrumbs: List[Dict[str, str]], base_url: str) -> Dict[str, Any]:
        """Generate breadcrumb schema markup."""
        breadcrumb_list = []
        
        for i, breadcrumb in enumerate(breadcrumbs, 1):
            breadcrumb_list.append({
                "@type": "ListItem",
                "position": i,
                "name": breadcrumb["name"],
                "item": urljoin(base_url, breadcrumb["url"])
            })
        
        return {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": breadcrumb_list
        }
    
    def generate_faq_schema(self, faqs: List[Dict[str, str]]) -> Dict[str, Any]:
        """Generate FAQ schema markup."""
        faq_list = []
        
        for faq in faqs:
            faq_list.append({
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["answer"]
                }
            })
        
        return {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_list
        }
    
    def generate_sitemap_data(
        self,
        base_url: str,
        pages: List[Dict[str, Any]],
        products: List[ProductSchema]
    ) -> List[Dict[str, Any]]:
        """Generate sitemap data for XML sitemap generation."""
        sitemap_urls = []
        
        # Static pages
        for page in pages:
            sitemap_urls.append({
                "loc": urljoin(base_url, page["url"]),
                "lastmod": datetime.now().isoformat(),
                "changefreq": page.get("changefreq", "weekly"),
                "priority": page.get("priority", "0.8")
            })
        
        # Product pages
        for product in products:
            sitemap_urls.append({
                "loc": urljoin(base_url, f"/product/{product.id}"),
                "lastmod": datetime.now().isoformat(),
                "changefreq": "daily",
                "priority": "0.6"
            })
        
        return sitemap_urls
    
    def generate_robots_txt(self, base_url: str, sitemap_url: Optional[str] = None) -> str:
        """Generate robots.txt content."""
        robots_content = """User-agent: *
Allow: /

# Disallow admin and API routes
Disallow: /api/
Disallow: /admin/
Disallow: /_next/
Disallow: /.*

# Allow important pages
Allow: /products
Allow: /categories
Allow: /search

# Crawl delay
Crawl-delay: 1

"""
        
        if sitemap_url:
            robots_content += f"Sitemap: {sitemap_url}\n"
        else:
            robots_content += f"Sitemap: {base_url}/sitemap.xml\n"
        
        return robots_content
    
    def optimize_images_metadata(self, images: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Optimize image metadata for SEO."""
        optimized_images = []
        
        for image in images:
            optimized = image.copy()
            
            # Generate SEO-friendly alt text if missing
            if not optimized.get('alt'):
                filename = image['src'].split('/')[-1].split('.')[0]
                optimized['alt'] = filename.replace('-', ' ').replace('_', ' ').title()
            
            # Add loading strategy
            optimized['loading'] = image.get('loading', 'lazy')
            
            # Add dimensions for better CLS
            if 'width' not in optimized or 'height' not in optimized:
                optimized['width'] = '400'
                optimized['height'] = '400'
            
            optimized_images.append(optimized)
        
        return optimized_images
    
    def generate_meta_tags(self, seo_data: SEOOptimization, page_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate all meta tags for a page."""
        meta_tags = {
            # Basic meta tags
            'title': seo_data.meta_title,
            'description': seo_data.meta_description,
            'keywords': ', '.join(seo_data.keywords),
            'viewport': 'width=device-width, initial-scale=1',
            'robots': 'index, follow',
            
            # Open Graph tags
            'og:title': seo_data.meta_title,
            'og:description': seo_data.meta_description,
            'og:type': 'website',
            'og:url': page_data.get('url', ''),
            'og:image': page_data.get('image', '/og-image.jpg'),
            'og:site_name': page_data.get('site_name', ''),
            
            # Twitter Card tags
            'twitter:card': 'summary_large_image',
            'twitter:title': seo_data.meta_title,
            'twitter:description': seo_data.meta_description,
            'twitter:image': page_data.get('image', '/twitter-image.jpg'),
            
            # Additional SEO tags
            'canonical': page_data.get('canonical_url', ''),
            'alternate': page_data.get('alternate_url', ''),
        }
        
        return {k: v for k, v in meta_tags.items() if v}  # Remove empty values