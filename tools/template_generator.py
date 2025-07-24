"""
Template generator for creating React/Next.js affiliate marketing websites.

This module uses Jinja2 to render templates with context-aware variable substitution
for branding, configuration, and research-informed design decisions.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from jinja2 import Environment, FileSystemLoader, Template
from agents.models import ConversionElement, NicheType, SEOOptimization


class TemplateGenerator:
    """Generates website files from Jinja2 templates with context injection."""
    
    def __init__(self, template_directory: str = "./templates"):
        self.template_dir = Path(template_directory)
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.env.filters['kebab_case'] = self._kebab_case
        self.env.filters['pascal_case'] = self._pascal_case
        self.env.filters['camel_case'] = self._camel_case
    
    def _kebab_case(self, text: str) -> str:
        """Convert text to kebab-case."""
        return text.lower().replace(' ', '-').replace('_', '-')
    
    def _pascal_case(self, text: str) -> str:
        """Convert text to PascalCase."""
        return ''.join(word.capitalize() for word in text.replace('-', ' ').replace('_', ' ').split())
    
    def _camel_case(self, text: str) -> str:
        """Convert text to camelCase."""
        pascal = self._pascal_case(text)
        return pascal[0].lower() + pascal[1:] if pascal else ''
    
    def generate_component(
        self,
        name: str,
        component_type: str,
        props: Dict[str, Any],
        styling: str,
        research_insights: List[ConversionElement] = None,
        niche: NicheType = NicheType.GENERAL
    ) -> str:
        """Generate React component with TypeScript and Tailwind."""
        template_path = f"react/components/{component_type}.tsx.template"
        
        try:
            template = self.env.get_template(template_path)
        except Exception:
            # Fallback to generic component template
            template = self.env.get_template("react/components/generic.tsx.template")
        
        context = {
            'name': name,
            'props': props,
            'styling': styling,
            'research_insights': research_insights or [],
            'niche': niche.value,
            'conversion_colors': self._get_conversion_colors(research_insights),
            'trust_signals': self._get_trust_signals(research_insights),
            'urgency_elements': self._get_urgency_elements(research_insights)
        }
        
        return template.render(**context)
    
    def generate_page(
        self,
        page_type: str,
        context: Dict[str, Any],
        seo_data: SEOOptimization = None
    ) -> str:
        """Generate Next.js page with SEO optimization."""
        template_path = f"nextjs/pages/{page_type}.tsx.template"
        
        try:
            template = self.env.get_template(template_path)
        except Exception:
            template = self.env.get_template("nextjs/pages/generic.tsx.template")
        
        page_context = {
            **context,
            'seo': seo_data.__dict__ if seo_data else {},
            'meta_tags': self._generate_meta_tags(seo_data) if seo_data else {},
            'structured_data': self._generate_structured_data(context, seo_data)
        }
        
        return template.render(**page_context)
    
    def generate_api_route(
        self,
        route_type: str,
        config: Dict[str, Any]
    ) -> str:
        """Generate Next.js API route."""
        template_path = f"nextjs/api/{route_type}.ts.template"
        
        try:
            template = self.env.get_template(template_path)
        except Exception:
            template = self.env.get_template("nextjs/api/generic.ts.template")
        
        return template.render(**config)
    
    def generate_config_file(
        self,
        config_type: str,
        context: Dict[str, Any]
    ) -> str:
        """Generate configuration files (package.json, tailwind.config.js, etc.)."""
        template_path = f"configs/{config_type}.template"
        
        try:
            template = self.env.get_template(template_path)
            return template.render(**context)
        except Exception as e:
            raise ValueError(f"Template not found: {template_path}") from e
    
    def generate_vercel_config(
        self,
        domain: str,
        environment_variables: Dict[str, str],
        build_config: Dict[str, Any] = None
    ) -> str:
        """Generate Vercel deployment configuration."""
        template = self.env.get_template("vercel/vercel.json.template")
        
        context = {
            'domain': domain,
            'env_vars': environment_variables,
            'build_config': build_config or {},
            'functions': self._get_vercel_functions_config(),
            'redirects': self._get_seo_redirects()
        }
        
        return template.render(**context)
    
    def _get_conversion_colors(self, insights: List[ConversionElement]) -> Dict[str, str]:
        """Extract conversion-optimized colors from research insights."""
        colors = {
            'primary': 'blue-600',
            'secondary': 'gray-600', 
            'accent': 'green-500',
            'warning': 'yellow-500',
            'danger': 'red-500'
        }
        
        if insights:
            for insight in insights:
                if 'green' in insight.color_scheme.lower():
                    colors['primary'] = 'green-600'
                elif 'orange' in insight.color_scheme.lower():
                    colors['primary'] = 'orange-600'
                elif 'red' in insight.color_scheme.lower():
                    colors['accent'] = 'red-600'
        
        return colors
    
    def _get_trust_signals(self, insights: List[ConversionElement]) -> List[str]:
        """Extract trust signals from research insights."""
        default_signals = [
            'SSL Secure Checkout',
            '30-Day Money Back Guarantee',
            'Free Shipping',
            'Customer Reviews'
        ]
        
        if insights:
            for insight in insights:
                if 'trust' in insight.psychology_principle.lower():
                    default_signals.append(insight.text_content)
        
        return default_signals
    
    def _get_urgency_elements(self, insights: List[ConversionElement]) -> List[str]:
        """Extract urgency elements from research insights."""
        default_urgency = [
            'Limited Time Offer',
            'Only X Left in Stock',
            'Sale Ends Soon'
        ]
        
        if insights:
            for insight in insights:
                if 'urgency' in insight.psychology_principle.lower() or 'scarcity' in insight.psychology_principle.lower():
                    default_urgency.append(insight.text_content)
        
        return default_urgency
    
    def _generate_meta_tags(self, seo_data: SEOOptimization) -> Dict[str, str]:
        """Generate meta tags for SEO."""
        return {
            'title': seo_data.meta_title,
            'description': seo_data.meta_description,
            'keywords': ', '.join(seo_data.keywords),
            'og:title': seo_data.meta_title,
            'og:description': seo_data.meta_description,
            'twitter:title': seo_data.meta_title,
            'twitter:description': seo_data.meta_description
        }
    
    def _generate_structured_data(self, context: Dict[str, Any], seo_data: SEOOptimization = None) -> Dict[str, Any]:
        """Generate JSON-LD structured data for SEO."""
        base_schema = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": context.get('brand_name', 'Affiliate Store'),
            "description": seo_data.meta_description if seo_data else context.get('description'),
            "url": context.get('domain', 'https://example.com')
        }
        
        # Add product schema if products are present
        if context.get('products'):
            base_schema["@type"] = "Store"
            base_schema["hasOfferCatalog"] = {
                "@type": "OfferCatalog",
                "name": "Product Catalog",
                "itemListElement": []
            }
        
        return base_schema
    
    def _get_vercel_functions_config(self) -> Dict[str, Any]:
        """Get Vercel functions configuration."""
        return {
            "app/api/sheets/route.ts": {
                "runtime": "nodejs18.x",
                "memory": 1024
            }
        }
    
    def _get_seo_redirects(self) -> List[Dict[str, str]]:
        """Get SEO-friendly redirects."""
        return [
            {
                "source": "/products",
                "destination": "/category/all",
                "permanent": False
            }
        ]
    
    def validate_typescript(self, code: str) -> bool:
        """Validate TypeScript syntax (basic check)."""
        # Basic validation - check for common syntax errors
        required_patterns = ['export', 'interface', 'type', 'const', 'function']
        syntax_errors = ['</script>', 'document.write', 'eval(']
        
        # Check for required patterns in React components
        has_export = any(pattern in code for pattern in ['export default', 'export const', 'export function'])
        
        # Check for syntax errors
        has_errors = any(error in code for error in syntax_errors)
        
        # Basic bracket matching
        open_braces = code.count('{')
        close_braces = code.count('}')
        
        return has_export and not has_errors and open_braces == close_braces