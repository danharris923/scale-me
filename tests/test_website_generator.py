"""
Tests for Website Generator Agent.

Comprehensive test suite covering the main website generation functionality,
tool integration, and output validation.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from pathlib import Path

from agents.website_generator_agent import WebsiteGeneratorAgent
from agents.models import (
    WebsiteGenerationRequest, 
    GoogleSheetsConfig, 
    NicheType, 
    AgentDependencies,
    GeneratedWebsite
)
from config.settings import Settings


class TestWebsiteGeneratorAgent:
    """Test suite for Website Generator Agent."""
    
    @pytest.fixture
    def settings(self):
        """Create test settings."""
        return Settings(
            output_directory="./test_generated",
            template_directory="./templates"
        )
    
    @pytest.fixture
    def agent(self, settings):
        """Create Website Generator Agent instance."""
        return WebsiteGeneratorAgent(settings)
    
    @pytest.fixture
    def sample_request(self):
        """Create sample website generation request."""
        sheets_config = GoogleSheetsConfig(
            sheet_id="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
            range_name="Sheet1!A:G"
        )
        
        return WebsiteGenerationRequest(
            niche=NicheType.TECH,
            brand_name="TechDeals Pro",
            target_audience="Tech enthusiasts seeking deals",
            sheets_config=sheets_config,
            color_scheme="blue",
            features=["responsive_design", "seo_optimized"],
            conversion_goals=["maximize_clicks", "build_trust"]
        )
    
    @pytest.fixture
    def sample_deps(self):
        """Create sample agent dependencies."""
        return AgentDependencies(
            output_directory="./test_generated",
            template_directory="./templates"
        )
    
    def test_agent_initialization(self, settings):
        """Test that agent initializes correctly with proper settings."""
        agent = WebsiteGeneratorAgent(settings)
        
        assert agent.settings == settings
        assert agent.provider is not None
        assert agent.research_agent is not None
        assert agent.file_generator is not None
        assert agent.seo_optimizer is not None
        assert agent.sheets_tool is not None
        assert agent.agent is not None
    
    def test_agent_initialization_with_defaults(self):
        """Test that agent initializes with default settings."""
        agent = WebsiteGeneratorAgent()
        
        assert agent.settings is not None
        assert isinstance(agent.settings, Settings)
    
    def test_system_prompt_generation(self, agent):
        """Test that system prompt is generated correctly."""
        system_prompt = agent._get_system_prompt()
        
        assert isinstance(system_prompt, str)
        assert len(system_prompt) > 100
        assert "React" in system_prompt
        assert "Next.js" in system_prompt
        assert "Tailwind CSS" in system_prompt
        assert "conversion optimization" in system_prompt
        assert "90+ Lighthouse scores" in system_prompt
    
    @pytest.mark.asyncio
    async def test_ui_research_tool(self, agent, sample_deps):
        """Test the UI research tool functionality."""
        with patch.object(agent.research_agent, 'quick_research') as mock_research:
            # Mock research result
            mock_result = Mock()
            mock_result.confidence_score = 0.85
            mock_result.findings = ["Finding 1", "Finding 2"]
            mock_result.recommendations = [
                Mock(
                    element_type="button",
                    psychology_principle="urgency",
                    color_scheme="red for action",
                    placement="above fold"
                )
            ]
            mock_research.return_value = mock_result
            
            # Test the tool through agent's tool registry
            tools = agent.agent.tools
            ui_research_tool = None
            for tool in tools:
                if tool.name == "get_ui_research":
                    ui_research_tool = tool
                    break
            
            assert ui_research_tool is not None
            
            # Mock RunContext
            ctx = Mock()
            ctx.deps = sample_deps
            
            result = await ui_research_tool.call(
                ctx=ctx,
                niche="tech",
                focus_area="ui_ux",
                target_audience="Tech enthusiasts"
            )
            
            assert isinstance(result, str)
            assert "Research Results" in result
            assert "Confidence Score: 0.85" in result
            assert "Finding 1" in result
    
    @pytest.mark.asyncio
    async def test_seo_strategy_tool(self, agent, sample_deps):
        """Test the SEO strategy generation tool."""
        with patch.object(agent.seo_optimizer, 'generate_seo_optimization') as mock_seo:
            # Mock SEO result
            mock_seo_data = Mock()
            mock_seo_data.meta_title = "Test Title"
            mock_seo_data.meta_description = "Test Description"
            mock_seo_data.keywords = ["tech", "deals"]
            mock_seo_data.schema_markup = {"website": {"@type": "WebSite"}}
            mock_seo_data.performance_targets = {"lighthouse_score": 90.0}
            mock_seo.return_value = mock_seo_data
            
            # Find SEO strategy tool
            seo_tool = None
            for tool in agent.agent.tools:
                if tool.name == "generate_seo_strategy":
                    seo_tool = tool
                    break
            
            assert seo_tool is not None
            
            ctx = Mock()
            ctx.deps = sample_deps
            
            result = await seo_tool.call(
                ctx=ctx,
                brand_name="TechDeals Pro",
                niche="tech",
                target_keywords=["tech deals", "electronics"],
                description="Best tech deals online"
            )
            
            assert isinstance(result, str)
            assert "SEO Strategy" in result
            assert "Test Title" in result
            assert "Test Description" in result
    
    @pytest.mark.asyncio
    async def test_sheets_integration_tool(self, agent, sample_deps):
        """Test the Google Sheets integration tool."""
        with patch.object(agent.sheets_tool, 'test_connection') as mock_test:
            # Mock successful connection
            mock_test.return_value = {
                'success': True,
                'headers': ['Name', 'Price', 'URL'],
                'message': 'Connection successful'
            }
            
            # Find sheets test tool
            sheets_tool = None
            for tool in agent.agent.tools:
                if tool.name == "test_sheets_integration":
                    sheets_tool = tool
                    break
            
            assert sheets_tool is not None
            
            ctx = Mock()
            ctx.deps = sample_deps
            
            result = await sheets_tool.call(
                ctx=ctx,
                sheet_id="test_sheet_id",
                range_name="Sheet1!A:C",
                api_key="test_api_key"
            )
            
            assert isinstance(result, str)
            assert "✅ Google Sheets Integration Test PASSED" in result
            assert "test_sheet_id" in result
    
    @pytest.mark.asyncio
    async def test_sheets_integration_tool_failure(self, agent, sample_deps):
        """Test the Google Sheets integration tool with failure."""
        with patch.object(agent.sheets_tool, 'test_connection') as mock_test:
            # Mock failed connection
            mock_test.return_value = {
                'success': False,
                'message': 'Invalid sheet ID'
            }
            
            sheets_tool = None
            for tool in agent.agent.tools:
                if tool.name == "test_sheets_integration":
                    sheets_tool = tool
                    break
            
            ctx = Mock()
            ctx.deps = sample_deps
            
            result = await sheets_tool.call(
                ctx=ctx,
                sheet_id="invalid_sheet_id",
                range_name="Sheet1!A:C"
            )
            
            assert isinstance(result, str)
            assert "❌ Google Sheets Integration Test FAILED" in result
            assert "Invalid sheet ID" in result
    
    @pytest.mark.asyncio
    async def test_file_generation_tool(self, agent, sample_deps):
        """Test the file generation tool."""
        with patch.object(agent.file_generator, 'generate_website') as mock_generate:
            # Mock generated website
            mock_website = Mock()
            mock_website.project_name = "test-project"
            mock_website.file_structure = {
                "pages/index.tsx": "// React component",
                "components/Hero.tsx": "// Hero component"
            }
            mock_website.environment_variables = {"API_KEY": "test_key"}
            mock_generate.return_value = mock_website
            
            # Find file generation tool
            file_tool = None
            for tool in agent.agent.tools:
                if tool.name == "generate_website_files":
                    file_tool = tool
                    break
            
            assert file_tool is not None
            
            ctx = Mock()
            ctx.deps = sample_deps
            
            request_data = {
                'niche': 'tech',
                'brand_name': 'Test Brand',
                'target_audience': 'Test Audience',
                'sheets_config': {
                    'sheet_id': 'test_id',
                    'range_name': 'Sheet1!A:G'
                }
            }
            
            result = await file_tool.call(
                ctx=ctx,
                request_data=request_data
            )
            
            assert isinstance(result, str)
            assert "✅ Website Generation COMPLETED" in result
            assert "test-project" in result
            assert "Files Generated: 2" in result
    
    @pytest.mark.asyncio
    async def test_website_validation_tool(self, agent, sample_deps):
        """Test the website validation tool."""
        with patch.object(agent.file_generator, 'validate_generated_files') as mock_validate:
            # Mock validation results
            mock_validate.return_value = {
                "pages/index.tsx": True,
                "components/Hero.tsx": True,
                "package.json": False
            }
            
            with patch('pathlib.Path.exists') as mock_exists:
                mock_exists.return_value = True
                
                # Find validation tool
                validation_tool = None
                for tool in agent.agent.tools:
                    if tool.name == "validate_generated_website":
                        validation_tool = tool
                        break
                
                assert validation_tool is not None
                
                ctx = Mock()
                ctx.deps = sample_deps
                
                result = await validation_tool.call(
                    ctx=ctx,
                    project_name="test-project"
                )
                
                assert isinstance(result, str)
                assert "🔍 Website Validation Results" in result
                assert "Files Validated: 3" in result
                assert "Passed: 2" in result
                assert "Failed: 1" in result
    
    @pytest.mark.asyncio
    async def test_complete_website_generation(self, agent, sample_request, sample_deps):
        """Test complete website generation process."""
        with patch.object(agent.agent, 'run') as mock_run:
            # Mock agent run result
            mock_result = Mock()
            mock_result.data = GeneratedWebsite(
                project_name="techdeals-pro",
                file_structure={"pages/index.tsx": "// React component"},
                package_json={"name": "techdeals-pro"},
                vercel_config={"version": 2},
                environment_variables={"API_KEY": "test"}
            )
            mock_run.return_value = mock_result
            
            result = await agent.generate_complete_website(sample_request, sample_deps)
            
            assert isinstance(result, GeneratedWebsite)
            assert result.project_name == "techdeals-pro"
            assert "pages/index.tsx" in result.file_structure
            
            # Verify the agent was called with proper prompt
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert "TechDeals Pro" in call_args[0][0]  # First positional arg is prompt
            assert "tech" in call_args[0][0]
            assert call_args[1]['deps'] == sample_deps  # deps passed as keyword arg
    
    @pytest.mark.asyncio
    async def test_quick_generate(self, agent):
        """Test quick website generation with minimal configuration."""
        with patch.object(agent, 'generate_complete_website') as mock_generate:
            mock_result = GeneratedWebsite(
                project_name="test-brand",
                file_structure={"pages/index.tsx": "// Component"},
                package_json={"name": "test-brand"},
                vercel_config={"version": 2},
                environment_variables={}
            )
            mock_generate.return_value = mock_result
            
            result = await agent.quick_generate(
                brand_name="Test Brand",
                niche="tech",
                target_audience="Tech users",
                sheet_id="test_sheet_id"
            )
            
            assert isinstance(result, GeneratedWebsite)
            assert result.project_name == "test-brand"
            
            # Verify generate_complete_website was called
            mock_generate.assert_called_once()
            call_args = mock_generate.call_args[0]
            request = call_args[0]
            assert request.brand_name == "Test Brand"
            assert request.niche == NicheType.TECH
            assert request.sheets_config.sheet_id == "test_sheet_id"
    
    @pytest.mark.asyncio
    async def test_error_handling_in_generation(self, agent, sample_request, sample_deps):
        """Test error handling during website generation."""
        with patch.object(agent.agent, 'run') as mock_run:
            mock_run.side_effect = Exception("Test error")
            
            with pytest.raises(Exception) as exc_info:
                await agent.generate_complete_website(sample_request, sample_deps)
            
            assert "Test error" in str(exc_info.value)
    
    def test_tool_registration(self, agent):
        """Test that all required tools are registered."""
        tool_names = [tool.name for tool in agent.agent.tools]
        
        expected_tools = [
            "get_ui_research",
            "generate_seo_strategy", 
            "test_sheets_integration",
            "generate_website_files",
            "validate_generated_website"
        ]
        
        for expected_tool in expected_tools:
            assert expected_tool in tool_names
    
    @pytest.mark.asyncio
    async def test_niche_type_conversion_edge_cases(self, agent, sample_deps):
        """Test edge cases in niche type conversion."""
        # Test with invalid niche
        seo_tool = None
        for tool in agent.agent.tools:
            if tool.name == "generate_seo_strategy":
                seo_tool = tool
                break
        
        with patch.object(agent.seo_optimizer, 'generate_seo_optimization') as mock_seo:
            mock_seo_data = Mock()
            mock_seo_data.meta_title = "Test Title"
            mock_seo_data.meta_description = "Test Description"
            mock_seo_data.keywords = ["test"]
            mock_seo_data.schema_markup = {}
            mock_seo_data.performance_targets = {}
            mock_seo.return_value = mock_seo_data
            
            ctx = Mock()
            ctx.deps = sample_deps
            
            # Test with invalid niche - should default to GENERAL
            result = await seo_tool.call(
                ctx=ctx,
                brand_name="Test Brand",
                niche="invalid_niche",
                target_keywords=["test"],
                description="Test description"
            )
            
            assert isinstance(result, str)
            # Verify the seo_optimizer was called with GENERAL niche
            mock_seo.assert_called_once()
            call_args = mock_seo.call_args[1]  # keyword arguments
            assert call_args['niche'] == NicheType.GENERAL