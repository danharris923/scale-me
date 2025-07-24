"""
Core data structures for the multi-agent affiliate marketing website generator.

This module defines all Pydantic models used across the system for data validation,
serialization, and type safety.
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum


class NicheType(str, Enum):
    """Supported affiliate marketing niches."""
    OUTDOOR_GEAR = "outdoor_gear"
    FASHION = "fashion"
    TECH = "tech"
    HOME_IMPROVEMENT = "home_improvement"
    MUSIC = "music"
    GENERAL = "general"


class ConversionElement(BaseModel):
    """UI element optimized for conversion."""
    element_type: Literal["button", "card", "banner", "form"]
    psychology_principle: str = Field(..., description="Psychology principle applied")
    color_scheme: str = Field(..., description="Color psychology rationale")
    text_content: str = Field(..., description="Conversion-optimized copy")
    placement: str = Field(..., description="Optimal placement strategy")


class SEOOptimization(BaseModel):
    """SEO optimization recommendations."""
    meta_title: str = Field(..., max_length=60)
    meta_description: str = Field(..., max_length=160)
    keywords: List[str] = Field(..., min_items=3, max_items=10)
    schema_markup: Dict[str, Any] = Field(default_factory=dict)
    performance_targets: Dict[str, float] = Field(default_factory=lambda: {
        "lighthouse_score": 90.0,
        "ttfb": 800.0,  # milliseconds
        "lcp": 2500.0,  # milliseconds
        "cls": 0.1
    })


class GoogleSheetsConfig(BaseModel):
    """Google Sheets integration configuration."""
    sheet_id: str = Field(..., description="Google Sheets ID")
    range_name: str = Field(default="Sheet1!A:Z")
    api_key: Optional[str] = Field(None, description="API key for public sheets")
    service_account_path: Optional[str] = Field(None, description="Service account JSON path")
    cache_duration: int = Field(default=300, description="Cache duration in seconds")


class ProductSchema(BaseModel):
    """Product data structure from Google Sheets."""
    id: str
    name: str
    price: float
    image_url: HttpUrl
    affiliate_url: HttpUrl
    category: str
    description: Optional[str] = None
    discount_percent: Optional[float] = Field(None, ge=0, le=100)
    is_featured: bool = False
    stock_status: Literal["in_stock", "low_stock", "out_of_stock"] = "in_stock"


class WebsiteGenerationRequest(BaseModel):
    """Request to generate affiliate marketing website."""
    niche: NicheType
    brand_name: str = Field(..., min_length=2, max_length=50)
    domain_name: Optional[str] = None
    color_scheme: str = Field(default="blue", description="Primary color theme")
    target_audience: str = Field(..., description="Target customer description")
    sheets_config: GoogleSheetsConfig
    features: List[str] = Field(default_factory=lambda: [
        "product_catalog", "category_pages", "search", "mobile_responsive", "seo_optimized"
    ])
    conversion_goals: List[str] = Field(default_factory=lambda: [
        "maximize_clicks", "build_trust", "reduce_bounce_rate"
    ])


class GeneratedWebsite(BaseModel):
    """Complete generated website structure."""
    project_name: str
    file_structure: Dict[str, str] = Field(..., description="File path to content mapping")
    package_json: Dict[str, Any]
    vercel_config: Dict[str, Any]
    environment_variables: Dict[str, str]
    deployment_url: Optional[HttpUrl] = None
    performance_metrics: Optional[Dict[str, float]] = None
    generation_timestamp: datetime = Field(default_factory=datetime.now)


class ResearchQuery(BaseModel):
    """Research query for the Research Agent."""
    topic: str = Field(..., description="Research topic")
    focus_area: Literal["ui_ux", "conversion", "seo", "performance", "accessibility"]
    niche_context: Optional[NicheType] = None
    max_sources: int = Field(default=5, ge=1, le=20)
    recency_days: int = Field(default=365, description="How recent should sources be")


class ResearchResult(BaseModel):
    """Research findings from Research Agent."""
    query: str
    findings: List[str] = Field(..., min_items=1)
    sources: List[HttpUrl] = Field(default_factory=list)
    recommendations: List[ConversionElement] = Field(default_factory=list)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    research_timestamp: datetime = Field(default_factory=datetime.now)


class AgentDependencies(BaseModel):
    """Dependencies injected into agents."""
    api_keys: Dict[str, str] = Field(default_factory=dict)
    output_directory: str = Field(default="./generated")
    template_directory: str = Field(default="./templates")
    research_cache: Dict[str, Any] = Field(default_factory=dict)
    performance_targets: SEOOptimization = Field(default_factory=SEOOptimization)