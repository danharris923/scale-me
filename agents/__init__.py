"""
Multi-agent system for generating affiliate marketing websites.

This package contains the core agents:
- WebsiteGeneratorAgent: Primary agent that orchestrates website generation
- ResearchAgent: Specialized agent for UI/UX and conversion research
"""

from .models import (
    NicheType,
    ConversionElement,
    SEOOptimization,
    GoogleSheetsConfig,
    ProductSchema,
    WebsiteGenerationRequest,
    GeneratedWebsite,
    ResearchQuery,
    ResearchResult,
    AgentDependencies,
)

__all__ = [
    "NicheType",
    "ConversionElement", 
    "SEOOptimization",
    "GoogleSheetsConfig",
    "ProductSchema",
    "WebsiteGenerationRequest",
    "GeneratedWebsite",
    "ResearchQuery",
    "ResearchResult",
    "AgentDependencies",
]