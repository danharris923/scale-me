"""
LLM provider configuration and management.

This module handles the configuration of different LLM providers
and provides fallback mechanisms as specified in the PRP.
"""

from typing import Dict, Optional, Any
from pydantic_ai import Agent
from config import Settings


class LLMProvider:
    """Manages LLM provider configuration and fallback logic."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self._models = {}
        self._initialize_models()
    
    def _initialize_models(self) -> None:
        """Initialize available models based on API keys."""
        if self.settings.openai_api_key:
            self._models["openai"] = f"openai:{self.settings.llm_model}"
        
        if self.settings.anthropic_api_key:
            # Map common model names to Anthropic equivalents
            anthropic_model = self._map_to_anthropic_model(self.settings.llm_model)
            self._models["anthropic"] = f"anthropic:{anthropic_model}"
        
        if self.settings.google_api_key:
            # Map to Google model names
            google_model = self._map_to_google_model(self.settings.llm_model)
            self._models["google"] = f"google:{google_model}"
    
    def _map_to_anthropic_model(self, model: str) -> str:
        """Map generic model names to Anthropic specific models."""
        mapping = {
            "gpt-4": "claude-3-5-sonnet-20241022",
            "gpt-4-turbo": "claude-3-5-sonnet-20241022", 
            "gpt-3.5-turbo": "claude-3-haiku-20240307"
        }
        return mapping.get(model, "claude-3-5-sonnet-20241022")
    
    def _map_to_google_model(self, model: str) -> str:
        """Map generic model names to Google specific models."""
        mapping = {
            "gpt-4": "gemini-1.5-pro",
            "gpt-4-turbo": "gemini-1.5-pro",
            "gpt-3.5-turbo": "gemini-1.5-flash"
        }
        return mapping.get(model, "gemini-1.5-pro")
    
    def get_primary_model(self) -> str:
        """Get the primary model based on configuration."""
        provider = self.settings.llm_provider
        if provider in self._models:
            return self._models[provider]
        
        # Fallback to first available model
        if self._models:
            return list(self._models.values())[0]
        
        raise ValueError("No LLM models available. Please check your API keys.")
    
    def get_fallback_model(self) -> Optional[str]:
        """Get fallback model configuration."""
        available_models = list(self._models.values())
        primary = self.get_primary_model()
        
        # Return the second available model as fallback
        fallback_models = [m for m in available_models if m != primary]
        return fallback_models[0] if fallback_models else None
    
    def create_agent_with_fallback(
        self, 
        system_prompt: str,
        deps_type: type = None,
        output_type: type = None,
        **kwargs
    ) -> Agent:
        """Create an agent with primary model configuration."""
        primary_model = self.get_primary_model()
        
        # For now, use the primary model directly
        # Future versions may support fallback mechanisms
        
        return Agent(
            model=primary_model,
            system_prompt=system_prompt,
            deps_type=deps_type,
            output_type=output_type,
            **kwargs
        )
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about configured models."""
        return {
            "primary_model": self.get_primary_model(),
            "fallback_model": self.get_fallback_model(),
            "available_providers": list(self._models.keys()),
            "total_models": len(self._models)
        }