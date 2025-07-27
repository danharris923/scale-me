"""
Shared configuration management for the integrated site builder.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class IntegratedConfig(BaseSettings):
    """Main configuration for the integrated site builder system."""
    
    # AI Model Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")
    
    # Existing GCS Server Configuration
    gcs_server_url: str = Field(..., env="GCS_SERVER_URL")
    gcs_server_ip: str = Field(..., env="GCS_SERVER_IP")
    
    # Deployment Configuration
    vercel_token: Optional[str] = Field(None, env="VERCEL_TOKEN")
    gcp_project_id: Optional[str] = Field(None, env="GCP_PROJECT_ID")
    
    # Site Configuration
    site_niche: str = Field("outdoor-adventure", env="SITE_NICHE")
    site_theme: str = Field("adventure-optimized", env="SITE_THEME")
    brand_name: str = Field("Adventure Gear Pro", env="BRAND_NAME")
    target_audience: str = Field("Outdoor enthusiasts, hikers, and campers", env="TARGET_AUDIENCE")
    
    # Product Sources
    product_sources: str = Field("amazon,cabelas", env="PRODUCT_SOURCES")
    affiliate_programs: str = Field("amazon-associates,cabelas-affiliate", env="AFFILIATE_PROGRAMS")
    
    # Development Settings
    debug: bool = Field(False, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    output_directory: str = Field("./generated", env="OUTPUT_DIRECTORY")
    template_directory: str = Field("./templates", env="TEMPLATE_DIRECTORY")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class SiteConfig(BaseModel):
    """Configuration for site generation."""
    
    niche: str
    theme: str
    brand_name: str
    tagline: str
    description: str
    target_audience: str
    primary_categories: list[str]
    
    @classmethod
    def load_from_file(cls, config_path: str) -> 'SiteConfig':
        """Load site configuration from JSON file."""
        with open(config_path, 'r') as f:
            data = json.load(f)
        return cls(**data['site_config'])


class DesignConfig(BaseModel):
    """Design configuration for site generation."""
    
    color_scheme: Dict[str, str]
    typography: Dict[str, str]
    layout: str
    hero_style: str
    card_style: str
    
    @classmethod
    def load_from_file(cls, config_path: str) -> 'DesignConfig':
        """Load design configuration from JSON file."""
        with open(config_path, 'r') as f:
            data = json.load(f)
        return cls(**data['design_config'])


class APIConfig(BaseModel):
    """API integration configuration."""
    
    data_sources: list[str]
    update_frequency: str
    cache_duration: str
    fallback_enabled: bool
    product_filters: Dict[str, Any]
    
    @classmethod
    def load_from_file(cls, config_path: str) -> 'APIConfig':
        """Load API configuration from JSON file."""
        with open(config_path, 'r') as f:
            data = json.load(f)
        return cls(**data['api_integration'])


def load_niche_config(niche: str) -> Dict[str, Any]:
    """Load complete configuration for a specific niche."""
    config_dir = Path(__file__).parent.parent / "config"
    config_file = config_dir / f"{niche}.json"
    
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    
    with open(config_file, 'r') as f:
        return json.load(f)


def get_server_status(gcs_url: str) -> Dict[str, Any]:
    """Check the status of the GCS server."""
    import requests
    
    try:
        # Check health endpoint
        health_response = requests.get(f"{gcs_url}/health", timeout=10)
        health_status = health_response.status_code == 200
        
        # Check products endpoint
        products_response = requests.get(f"{gcs_url}/products", timeout=10)
        if products_response.status_code == 200:
            products_data = products_response.json()
            products_count = products_data.get("count", 0)
        else:
            products_count = 0
        
        # Check available sites
        sites_response = requests.get(f"{gcs_url}/sites", timeout=10)
        if sites_response.status_code == 200:
            sites_data = sites_response.json()
            available_sites = sites_data.get("sites", [])
        else:
            available_sites = []
        
        return {
            "healthy": health_status,
            "products_count": products_count,
            "available_sites": available_sites,
            "url": gcs_url,
            "last_checked": "now"
        }
        
    except Exception as e:
        return {
            "healthy": False,
            "error": str(e),
            "url": gcs_url,
            "last_checked": "now"
        }


def validate_existing_server(gcs_url: str) -> bool:
    """Validate that the existing GCS server is working properly."""
    status = get_server_status(gcs_url)
    
    if not status["healthy"]:
        print(f"❌ GCS Server not healthy: {status.get('error', 'Unknown error')}")
        return False
    
    if status["products_count"] < 1:
        print(f"❌ No products found on server. Products count: {status['products_count']}")
        return False
    
    expected_sources = ["amazon", "cabelas"]
    available_sites = status["available_sites"]
    
    if not any(source in str(available_sites).lower() for source in expected_sources):
        print(f"❌ Expected product sources not found. Available: {available_sites}")
        return False
    
    print(f"✅ GCS Server is healthy!")
    print(f"   Products: {status['products_count']}")
    print(f"   Sites: {available_sites}")
    
    return True