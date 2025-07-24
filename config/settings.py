"""
Configuration settings for the affiliate marketing website generator.

Uses pydantic-settings to load environment variables with validation
and provide fallback defaults for development.
"""

import os
from typing import Dict, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # LLM Provider Configuration
    llm_provider: str = Field(default="openai", description="Primary LLM provider")
    llm_model: str = Field(default="gpt-4", description="LLM model to use")
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")
    google_api_key: Optional[str] = Field(default=None, description="Google AI API key")
    
    # Google Sheets Configuration
    google_sheets_api_key: Optional[str] = Field(default=None, description="Google Sheets API key")
    google_sheets_service_account: Optional[str] = Field(
        default=None, 
        description="Path to Google service account JSON"
    )
    
    # Web Research Configuration
    serpapi_key: Optional[str] = Field(default=None, description="SerpAPI key for web research")
    brave_search_key: Optional[str] = Field(default=None, description="Brave Search API key")
    
    # Application Configuration
    output_directory: str = Field(default="./generated", description="Output directory for generated websites")
    template_directory: str = Field(default="./templates", description="Template directory")
    log_level: str = Field(default="INFO", description="Logging level")
    
    # Performance Configuration
    max_concurrent_requests: int = Field(default=5, description="Max concurrent API requests")
    request_timeout: int = Field(default=30, description="Request timeout in seconds")
    cache_ttl: int = Field(default=3600, description="Cache TTL in seconds")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @validator("llm_provider")
    def validate_llm_provider(cls, v):
        """Validate LLM provider is supported."""
        supported_providers = ["openai", "anthropic", "google", "groq"]
        if v not in supported_providers:
            raise ValueError(f"LLM provider must be one of: {supported_providers}")
        return v
    
    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()
    
    @property
    def api_keys(self) -> Dict[str, str]:
        """Get all configured API keys."""
        keys = {}
        if self.openai_api_key:
            keys["openai"] = self.openai_api_key
        if self.anthropic_api_key:
            keys["anthropic"] = self.anthropic_api_key
        if self.google_api_key:
            keys["google"] = self.google_api_key
        if self.google_sheets_api_key:
            keys["google_sheets"] = self.google_sheets_api_key
        if self.serpapi_key:
            keys["serpapi"] = self.serpapi_key
        if self.brave_search_key:
            keys["brave_search"] = self.brave_search_key
        return keys
    
    def validate_required_keys(self) -> None:
        """Validate that required API keys are present."""
        if self.llm_provider == "openai" and not self.openai_api_key:
            raise ValueError("OpenAI API key required when using OpenAI provider")
        if self.llm_provider == "anthropic" and not self.anthropic_api_key:
            raise ValueError("Anthropic API key required when using Anthropic provider")
        if self.llm_provider == "google" and not self.google_api_key:
            raise ValueError("Google API key required when using Google provider")
    
    def get_model_config(self) -> Dict[str, str]:
        """Get model configuration for the selected provider."""
        return {
            "provider": self.llm_provider,
            "model": self.llm_model,
            "api_key": self.api_keys.get(self.llm_provider)
        }