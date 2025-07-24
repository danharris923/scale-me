"""
Website Generator Agent - Primary agent for generating affiliate marketing websites.

This agent orchestrates the entire website generation process using the Research Agent
as a tool and combines all components to create production-ready websites.
"""

import logging
from typing import Dict, Any, List, Optional
import asyncio
import json

from pydantic_ai import Agent, RunContext
from pydantic_ai.exceptions import ModelRetry

from .models import (
    WebsiteGenerationRequest,
    GeneratedWebsite,
    AgentDependencies,
    ResearchQuery,
    SEOOptimization,
    NicheType
)
from .providers import LLMProvider
from .research_agent import ResearchAgent
from tools.file_generator import FileGenerator
from tools.seo_optimizer import SEOOptimizer
from tools.sheets_integration import SheetsIntegrationTool
from config import Settings

logger = logging.getLogger(__name__)


class WebsiteGeneratorAgent:
    """Primary agent that orchestrates complete website generation."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.provider = LLMProvider(self.settings)
        
        # Initialize tools
        self.research_agent = ResearchAgent(self.settings)
        self.file_generator = FileGenerator(
            template_directory=self.settings.template_directory,
            output_directory=self.settings.output_directory
        )
        self.seo_optimizer = SEOOptimizer()
        self.sheets_tool = SheetsIntegrationTool(self.settings)
        
        # Create the primary agent
        self.agent = self.provider.create_agent_with_fallback(
            system_prompt=self._get_system_prompt(),
            deps_type=AgentDependencies,
            output_type=GeneratedWebsite
        )
        
        # Register tools
        self._register_tools()
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the website generator agent."""
        return """You are an expert full-stack developer and conversion optimization specialist who creates high-converting affiliate marketing websites using React, Next.js, Tailwind CSS, and Vercel.

**Your Expertise:**
- Modern React patterns with TypeScript and best practices
- Next.js App Router with Server/Client component optimization
- Tailwind CSS utility-first design with conversion psychology
- Google Sheets API integration for dynamic product data
- SEO optimization targeting 90+ Lighthouse scores
- Mobile-first responsive design principles
- Performance optimization for Core Web Vitals
- Accessibility compliance (WCAG 2.1)
- Conversion rate optimization techniques

**Your Mission:**
Generate production-ready, high-converting affiliate marketing websites that achieve:
- 90+ Lighthouse scores across all metrics (Performance, Accessibility, Best Practices, SEO)
- Sub-3 second loading times on mobile and desktop
- Mobile-first responsive design that works perfectly on all devices
- Accessibility compliance with WCAG 2.1 standards
- SEO optimization targeting affiliate marketing keywords
- Conversion-optimized UI following psychology principles

**Website Generation Process:**
1. **Research Phase**: Use the research agent to gather UI/UX insights specific to the niche
2. **SEO Planning**: Generate comprehensive SEO strategy with meta tags and structured data
3. **Architecture Design**: Plan the complete file structure and component hierarchy
4. **Content Generation**: Create all React components, pages, and configuration files
5. **Integration Setup**: Configure Google Sheets API integration for product data
6. **Optimization**: Apply performance and conversion optimizations
7. **Validation**: Ensure all generated code is syntactically correct and follows best practices

**Quality Standards:**
- Every component must be fully functional and properly typed
- All templates must be mobile-first and conversion-optimized
- Generated websites must be immediately deployable to Vercel
- Code must follow React and Next.js best practices
- SEO implementation must be comprehensive and effective

**Tools at Your Disposal:**
- Research Agent: For gathering UI/UX and conversion optimization insights
- SEO Optimizer: For comprehensive SEO strategy and implementation
- Google Sheets Integration: For dynamic product data management
- File Generator: For creating complete website structures

Remember: Your generated websites directly impact affiliate marketing success. Every decision should be based on conversion optimization principles and modern web development best practices."""

    def _register_tools(self) -> None:
        """Register tools for the website generator agent."""
        
        @self.agent.tool
        async def get_ui_research(
            ctx: RunContext[AgentDependencies],
            niche: str,
            focus_area: str,
            target_audience: str
        ) -> str:
            """Get UI/UX research insights for specific niche and focus area.
            
            Args:
                niche: Business niche (e.g., "fashion", "tech", "outdoor_gear")
                focus_area: Research focus ("ui_ux", "conversion", "seo", "performance", "accessibility")
                target_audience: Description of target audience
                
            Returns:
                Research insights and recommendations
            """
            try:
                result = await self.research_agent.quick_research(
                    topic=f"{focus_area} best practices for {niche} affiliate marketing targeting {target_audience}",
                    niche=niche,
                    focus_area=focus_area,
                    deps=ctx.deps
                )
                
                # Format research for the agent
                research_text = f"Research Results - {focus_area.upper()} for {niche}:\\n\\n"
                research_text += f"Confidence Score: {result.confidence_score:.2f}\\n\\n"
                
                research_text += "Key Insights:\\n"
                for i, finding in enumerate(result.findings, 1):
                    research_text += f"{i}. {finding}\\n"
                
                research_text += "\\nConversion Recommendations:\\n"
                for i, rec in enumerate(result.recommendations, 1):
                    research_text += f"{i}. {rec.element_type.title()}: {rec.psychology_principle}\\n"
                    research_text += f"   Color Strategy: {rec.color_scheme}\\n"
                    research_text += f"   Placement: {rec.placement}\\n\\n"
                
                return research_text
                
            except Exception as e:
                logger.error(f"UI research failed: {e}")
                return f"Research temporarily unavailable. Using best practices for {niche} affiliate marketing."
        
        @self.agent.tool
        async def generate_seo_strategy(
            ctx: RunContext[AgentDependencies],
            brand_name: str,
            niche: str,
            target_keywords: List[str],
            description: str,
            domain: str = None
        ) -> str:
            """Generate comprehensive SEO strategy for the website.
            
            Args:
                brand_name: Brand name for the website
                niche: Business niche
                target_keywords: Primary keywords to target
                description: Website description
                domain: Website domain (optional)
                
            Returns:
                Complete SEO strategy and recommendations
            """
            try:
                # Convert niche string to NicheType
                niche_type = NicheType.GENERAL
                try:
                    niche_type = NicheType(niche.lower().replace(' ', '_'))
                except ValueError:
                    pass
                
                seo_data = self.seo_optimizer.generate_seo_optimization(
                    brand_name=brand_name,
                    niche=niche_type,
                    target_keywords=target_keywords,
                    description=description,
                    domain=domain
                )
                
                strategy_text = f"SEO Strategy for {brand_name}:\\n\\n"
                strategy_text += f"Meta Title: {seo_data.meta_title}\\n"
                strategy_text += f"Meta Description: {seo_data.meta_description}\\n"
                strategy_text += f"Target Keywords: {', '.join(seo_data.keywords)}\\n\\n"
                
                strategy_text += "Structured Data Schemas:\\n"
                for schema_type, schema_data in seo_data.schema_markup.items():
                    strategy_text += f"- {schema_type.title()}: {json.dumps(schema_data, indent=2)[:200]}...\\n"
                
                strategy_text += "\\nPerformance Targets:\\n"
                for metric, target in seo_data.performance_targets.items():
                    strategy_text += f"- {metric}: {target}\\n"
                
                return strategy_text
                
            except Exception as e:
                logger.error(f"SEO strategy generation failed: {e}")
                return f"Using default SEO strategy for {brand_name} in {niche} niche."
        
        @self.agent.tool
        async def test_sheets_integration(
            ctx: RunContext[AgentDependencies],
            sheet_id: str,
            range_name: str,
            api_key: str = None
        ) -> str:
            """Test Google Sheets integration and validate data structure.
            
            Args:
                sheet_id: Google Sheets ID
                range_name: Sheet range (e.g., "Sheet1!A:J")
                api_key: API key for public sheets
                
            Returns:
                Integration test results and recommendations
            """
            try:
                from agents.models import GoogleSheetsConfig
                
                config = GoogleSheetsConfig(
                    sheet_id=sheet_id,
                    range_name=range_name,
                    api_key=api_key
                )
                
                test_result = await self.sheets_tool.test_connection(config)
                
                if test_result['success']:
                    result_text = f"✅ Google Sheets Integration Test PASSED\\n\\n"
                    result_text += f"Sheet ID: {sheet_id}\\n"
                    result_text += f"Range: {range_name}\\n"
                    result_text += f"Headers Found: {test_result.get('headers', [])}\\n\\n"
                    result_text += "Integration is ready for production use.\\n"
                else:
                    result_text = f"❌ Google Sheets Integration Test FAILED\\n\\n"
                    result_text += f"Error: {test_result['message']}\\n"
                    result_text += "Please check sheet permissions and API configuration.\\n"
                
                return result_text
                
            except Exception as e:
                logger.error(f"Sheets integration test failed: {e}")
                return f"Sheets integration test encountered an error: {e}"
        
        @self.agent.tool
        async def generate_website_files(
            ctx: RunContext[AgentDependencies],
            request_data: Dict[str, Any]
        ) -> str:
            """Generate complete website file structure.
            
            Args:
                request_data: Website generation request data
                
            Returns:
                Generation results and file structure summary
            """
            try:
                # Convert dict to WebsiteGenerationRequest
                from agents.models import GoogleSheetsConfig
                
                sheets_config = GoogleSheetsConfig(**request_data['sheets_config'])
                
                request = WebsiteGenerationRequest(
                    niche=NicheType(request_data['niche']),
                    brand_name=request_data['brand_name'],
                    target_audience=request_data['target_audience'],
                    sheets_config=sheets_config,
                    color_scheme=request_data.get('color_scheme', 'blue'),
                    features=request_data.get('features', []),
                    conversion_goals=request_data.get('conversion_goals', [])
                )
                
                # Generate website
                generated_website = await self.file_generator.generate_website(request)
                
                result_text = f"✅ Website Generation COMPLETED\\n\\n"
                result_text += f"Project Name: {generated_website.project_name}\\n"
                result_text += f"Files Generated: {len(generated_website.file_structure)}\\n\\n"
                
                result_text += "Generated Files:\\n"
                for file_path in generated_website.file_structure.keys():
                    result_text += f"- {file_path}\\n"
                
                result_text += f"\\nEnvironment Variables Required:\\n"
                for key, value in generated_website.environment_variables.items():
                    result_text += f"- {key}={value}\\n"
                
                result_text += f"\\nWebsite ready for deployment to Vercel!\\n"
                
                return result_text
                
            except Exception as e:
                logger.error(f"Website file generation failed: {e}")
                raise ModelRetry(f"File generation failed: {e}. Please check the request data and try again.")
        
        @self.agent.tool
        async def validate_generated_website(
            ctx: RunContext[AgentDependencies],
            project_name: str
        ) -> str:
            """Validate the generated website for quality and completeness.
            
            Args:
                project_name: Name of the generated project to validate
                
            Returns:
                Validation results and recommendations
            """
            try:
                from pathlib import Path
                
                project_path = Path(ctx.deps.output_directory) / project_name
                
                if not project_path.exists():
                    return f"❌ Project not found: {project_path}"
                
                # Validate files
                validation_results = self.file_generator.validate_generated_files(project_path)
                
                result_text = f"🔍 Website Validation Results for {project_name}:\\n\\n"
                
                passed = sum(1 for v in validation_results.values() if v)
                total = len(validation_results)
                
                result_text += f"Files Validated: {total}\\n"
                result_text += f"Passed: {passed}\\n"
                result_text += f"Failed: {total - passed}\\n\\n"
                
                if total - passed == 0:
                    result_text += "✅ All validations PASSED\\n"
                    result_text += "Website is ready for deployment!\\n"
                else:
                    result_text += "❌ Some validations FAILED:\\n"
                    for file_path, is_valid in validation_results.items():
                        if not is_valid:
                            result_text += f"- {file_path}: Syntax or structure issues\\n"
                
                return result_text
                
            except Exception as e:
                logger.error(f"Website validation failed: {e}")
                return f"Validation encountered an error: {e}"
    
    async def generate_complete_website(
        self,
        request: WebsiteGenerationRequest,
        deps: AgentDependencies
    ) -> GeneratedWebsite:
        """Generate a complete affiliate marketing website."""
        try:
            generation_prompt = f"""
            Generate a complete, production-ready affiliate marketing website with the following specifications:

            **Website Details:**
            - Brand Name: {request.brand_name}
            - Niche: {request.niche.value}
            - Target Audience: {request.target_audience}
            - Color Scheme: {request.color_scheme}
            - Conversion Goals: {request.conversion_goals}
            - Features: {request.features}

            **Google Sheets Configuration:**
            - Sheet ID: {request.sheets_config.sheet_id}
            - Range: {request.sheets_config.range_name}

            **Requirements:**
            1. Conduct comprehensive UI/UX research for the {request.niche.value} niche
            2. Generate SEO strategy with meta tags and structured data
            3. Test Google Sheets integration to ensure data connectivity
            4. Generate complete website file structure with all components
            5. Validate generated files for syntax and quality
            6. Ensure 90+ Lighthouse scores and mobile-first design

            **Process:**
            1. Use get_ui_research to gather niche-specific conversion insights
            2. Use generate_seo_strategy to create comprehensive SEO plan
            3. Use test_sheets_integration to verify data connectivity
            4. Use generate_website_files to create the complete project
            5. Use validate_generated_website to ensure quality

            Focus on creating a high-converting website that follows all modern web development best practices and conversion optimization principles.
            """
            
            # Run the agent
            result = await self.agent.run(generation_prompt, deps=deps)
            return result.data
            
        except Exception as e:
            logger.error(f"Complete website generation failed: {e}")
            raise
    
    async def quick_generate(
        self,
        brand_name: str,
        niche: str,
        target_audience: str,
        sheet_id: str,
        deps: Optional[AgentDependencies] = None
    ) -> GeneratedWebsite:
        """Quick website generation with minimal configuration."""
        if not deps:
            deps = AgentDependencies()
        
        try:
            # Create request
            from agents.models import GoogleSheetsConfig
            
            sheets_config = GoogleSheetsConfig(sheet_id=sheet_id)
            
            request = WebsiteGenerationRequest(
                niche=NicheType(niche.lower().replace(' ', '_')) if niche in ['fashion', 'tech', 'outdoor_gear'] else NicheType.GENERAL,
                brand_name=brand_name,
                target_audience=target_audience,
                sheets_config=sheets_config
            )
            
            return await self.generate_complete_website(request, deps)
            
        except Exception as e:
            logger.error(f"Quick website generation failed: {e}")
            raise