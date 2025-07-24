"""
Integration Tests for Multi-Agent Website Generation System.

Tests complete workflows, agent interactions, and end-to-end functionality
including website generation, file creation, and validation.
"""

import pytest
import asyncio
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch, MagicMock

from agents.website_generator_agent import WebsiteGeneratorAgent
from agents.research_agent import ResearchAgent
from agents.models import (
    WebsiteGenerationRequest,
    GoogleSheetsConfig,
    NicheType,
    AgentDependencies,
    GeneratedWebsite,
    ResearchResult,
    ConversionElement
)
from config.settings import Settings
from cli import CLIInterface


class TestEndToEndWebsiteGeneration:
    """Test complete website generation workflow."""
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def settings(self, temp_output_dir):
        """Create test settings with temporary directories."""
        return Settings(
            output_directory=temp_output_dir,
            template_directory="./templates"
        )
    
    @pytest.fixture
    def website_generator(self, settings):
        """Create website generator agent."""
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
            target_audience="Tech enthusiasts looking for the best deals",
            sheets_config=sheets_config,
            color_scheme="blue",
            features=["responsive_design", "seo_optimized", "conversion_focused"],
            conversion_goals=["maximize_clicks", "build_trust", "increase_engagement"]
        )
    
    @pytest.fixture
    def mock_research_result(self):
        """Create mock research result."""
        recommendations = [
            ConversionElement(
                element_type="button",
                psychology_principle="urgency/scarcity",
                color_scheme="red for action",
                text_content="Buy Now - Limited Time Offer!",
                placement="above the fold, right-aligned"
            ),
            ConversionElement(
                element_type="banner",
                psychology_principle="trust building",
                color_scheme="blue for professionalism",
                text_content="Trusted by 10,000+ customers",
                placement="top of page"
            )
        ]
        
        return ResearchResult(
            query="UI/UX and conversion optimization for tech affiliate marketing",
            findings=[
                "Red call-to-action buttons increase click-through rates by 21%",
                "Trust signals in headers improve conversion rates by 15%",
                "Mobile-first design is crucial for tech audience engagement",
                "Social proof elements should be prominently displayed",
                "Page load speed under 3 seconds is critical for tech users"
            ],
            sources=[
                "https://cxl.com/blog/button-color-psychology",
                "https://www.nngroup.com/articles/trust-and-credibility",
                "https://developers.google.com/web/fundamentals/performance"
            ],
            recommendations=recommendations,
            confidence_score=0.92,
            research_timestamp=asyncio.get_event_loop().time()
        )
    
    @pytest.mark.asyncio
    async def test_complete_website_generation_workflow(
        self, 
        website_generator, 
        sample_request, 
        temp_output_dir,
        mock_research_result
    ):
        """Test the complete website generation workflow."""
        deps = AgentDependencies(
            output_directory=temp_output_dir,
            template_directory="./templates"
        )
        
        # Mock the research agent responses
        with patch.object(website_generator.research_agent, 'quick_research') as mock_research:
            mock_research.return_value = mock_research_result
            
            # Mock Google Sheets integration
            with patch.object(website_generator.sheets_tool, 'test_connection') as mock_sheets:
                mock_sheets.return_value = {
                    'success': True,
                    'headers': ['Name', 'Description', 'Price', 'Image URL', 'Affiliate URL', 'Category', 'Stock Status'],
                    'message': 'Connection successful'
                }
                
                # Mock file generation
                with patch.object(website_generator.file_generator, 'generate_website') as mock_file_gen:
                    mock_website = GeneratedWebsite(
                        project_name="techdeals-pro",
                        file_structure={
                            "pages/index.tsx": "// Home page component\nimport React from 'react';\n\nconst HomePage = () => {\n  return <div>Welcome to TechDeals Pro</div>;\n};\n\nexport default HomePage;",
                            "components/ProductCard.tsx": "// Product card component",
                            "components/Hero.tsx": "// Hero section component", 
                            "components/Navigation.tsx": "// Navigation component",
                            "components/Footer.tsx": "// Footer component",
                            "pages/category/[slug].tsx": "// Dynamic category page",
                            "pages/api/sheets.ts": "// Google Sheets API route",
                            "package.json": json.dumps({
                                "name": "techdeals-pro",
                                "version": "1.0.0",
                                "dependencies": {
                                    "react": "^18.2.0",
                                    "next": "^14.0.0"
                                }
                            }),
                            "tailwind.config.js": "// Tailwind configuration",
                            "next.config.js": "// Next.js configuration",
                            "vercel.json": json.dumps({"version": 2})
                        },
                        package_json={
                            "name": "techdeals-pro",
                            "version": "1.0.0",
                            "dependencies": {
                                "react": "^18.2.0",
                                "next": "^14.0.0"
                            }
                        },
                        vercel_config={"version": 2},
                        environment_variables={
                            "GOOGLE_SHEETS_API_KEY": "your-google-sheets-api-key",
                            "NEXT_PUBLIC_BRAND_NAME": "TechDeals Pro",
                            "NEXT_PUBLIC_NICHE": "tech"
                        }
                    )
                    mock_file_gen.return_value = mock_website
                    
                    # Mock file validation
                    with patch.object(website_generator.file_generator, 'validate_generated_files') as mock_validate:
                        mock_validate.return_value = {
                            "pages/index.tsx": True,
                            "components/ProductCard.tsx": True,
                            "components/Hero.tsx": True,
                            "package.json": True
                        }
                        
                        # Execute the complete workflow
                        result = await website_generator.generate_complete_website(sample_request, deps)
                        
                        # Verify the result
                        assert isinstance(result, GeneratedWebsite)
                        assert result.project_name == "techdeals-pro"
                        assert len(result.file_structure) >= 8  # Should have multiple files
                        assert "pages/index.tsx" in result.file_structure
                        assert "components/ProductCard.tsx" in result.file_structure
                        assert "package.json" in result.file_structure
                        assert result.environment_variables["NEXT_PUBLIC_BRAND_NAME"] == "TechDeals Pro"
                        
                        # Verify research was conducted
                        mock_research.assert_called()
                        
                        # Verify sheets integration was tested
                        mock_sheets.assert_called()
                        
                        # Verify files were generated
                        mock_file_gen.assert_called()
                        
                        # Verify validation was performed
                        mock_validate.assert_called()
    
    @pytest.mark.asyncio
    async def test_agent_tool_interactions(self, website_generator, sample_request, temp_output_dir):
        """Test that agents properly use each other's tools."""
        deps = AgentDependencies(
            output_directory=temp_output_dir,
            template_directory="./templates"
        )
        
        with patch.object(website_generator.agent, 'run') as mock_agent_run:
            # Mock the agent run to simulate tool usage
            mock_result = Mock()
            mock_result.data = GeneratedWebsite(
                project_name="test-project",
                file_structure={"pages/index.tsx": "// Test content"},
                package_json={"name": "test"},
                vercel_config={"version": 2},
                environment_variables={}
            )
            mock_agent_run.return_value = mock_result
            
            result = await website_generator.generate_complete_website(sample_request, deps)
            
            # Verify the agent was called with the correct prompt structure
            mock_agent_run.assert_called_once()
            call_args = mock_agent_run.call_args
            prompt = call_args[0][0]
            
            # Verify prompt contains all required information
            assert "TechDeals Pro" in prompt
            assert "tech" in prompt
            assert "Tech enthusiasts" in prompt
            assert "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms" in prompt
            assert "get_ui_research" in prompt
            assert "generate_seo_strategy" in prompt
            assert "test_sheets_integration" in prompt
            assert "generate_website_files" in prompt
            assert "validate_generated_website" in prompt
    
    @pytest.mark.asyncio
    async def test_error_handling_in_workflow(self, website_generator, sample_request, temp_output_dir):
        """Test error handling throughout the workflow."""
        deps = AgentDependencies(
            output_directory=temp_output_dir,
            template_directory="./templates"
        )
        
        # Test research agent failure
        with patch.object(website_generator.research_agent, 'quick_research') as mock_research:
            mock_research.side_effect = Exception("Research service unavailable")
            
            # The system should handle research failures gracefully
            with patch.object(website_generator.agent, 'run') as mock_agent_run:
                mock_result = Mock()
                mock_result.data = GeneratedWebsite(
                    project_name="test-project",
                    file_structure={"pages/index.tsx": "// Test content"},
                    package_json={"name": "test"},
                    vercel_config={"version": 2},
                    environment_variables={}
                )
                mock_agent_run.return_value = mock_result
                
                result = await website_generator.generate_complete_website(sample_request, deps)
                assert isinstance(result, GeneratedWebsite)
    
    @pytest.mark.asyncio 
    async def test_quick_generate_integration(self, website_generator):
        """Test the quick generate method integration."""
        with patch.object(website_generator, 'generate_complete_website') as mock_complete:
            mock_result = GeneratedWebsite(
                project_name="quick-brand",
                file_structure={"pages/index.tsx": "// Quick content"},
                package_json={"name": "quick-brand"},
                vercel_config={"version": 2},
                environment_variables={}
            )
            mock_complete.return_value = mock_result
            
            result = await website_generator.quick_generate(
                brand_name="Quick Brand",
                niche="tech",
                target_audience="Tech users",
                sheet_id="test_sheet_id"
            )
            
            assert isinstance(result, GeneratedWebsite)
            assert result.project_name == "quick-brand"
            
            # Verify the request was properly constructed
            mock_complete.assert_called_once()
            request_arg = mock_complete.call_args[0][0]
            assert request_arg.brand_name == "Quick Brand"
            assert request_arg.niche == NicheType.TECH
            assert request_arg.sheets_config.sheet_id == "test_sheet_id"


class TestCLIIntegration:
    """Test CLI integration with the multi-agent system."""
    
    @pytest.fixture
    def cli_interface(self):
        """Create CLI interface for testing."""
        return CLIInterface()
    
    @pytest.fixture
    def mock_user_input_sequence(self):
        """Mock user input sequence for CLI."""
        return [
            "2",  # Tech niche
            "TechDeals Pro",  # Brand name
            "Tech enthusiasts seeking deals",  # Target audience
            "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",  # Sheet ID
            "Sheet1!A:G",  # Sheet range (default)
            "blue",  # Color scheme (default)
            "1,2,3"  # Conversion goals
        ]
    
    def test_cli_initialization(self):
        """Test CLI interface initialization."""
        cli = CLIInterface()
        
        assert cli.console is not None
        assert cli.settings is not None
        assert cli.generator is not None
        assert isinstance(cli.current_step, str)
        assert isinstance(cli.tool_calls, list)
    
    def test_display_welcome(self, cli_interface):
        """Test welcome display functionality."""
        # This should not raise any exceptions
        cli_interface.display_welcome()
    
    @pytest.mark.asyncio
    async def test_get_user_configuration_flow(self, cli_interface, mock_user_input_sequence):
        """Test user configuration gathering."""
        with patch('rich.prompt.Prompt.ask') as mock_prompt:
            with patch('rich.prompt.Confirm.ask') as mock_confirm:
                # Setup mock responses
                mock_prompt.side_effect = mock_user_input_sequence
                mock_confirm.return_value = True
                
                request = await cli_interface.get_user_configuration()
                
                assert isinstance(request, WebsiteGenerationRequest)
                assert request.niche == NicheType.TECH
                assert request.brand_name == "TechDeals Pro"
                assert request.target_audience == "Tech enthusiasts seeking deals"
                assert request.sheets_config.sheet_id == "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
                assert request.color_scheme == "blue"
    
    @pytest.mark.asyncio
    async def test_generate_website_with_streaming(self, cli_interface):
        """Test website generation with streaming output."""
        sample_request = WebsiteGenerationRequest(
            niche=NicheType.TECH,
            brand_name="Test Brand",
            target_audience="Test Audience",
            sheets_config=GoogleSheetsConfig(sheet_id="test_id"),
            color_scheme="blue",
            features=["responsive_design"],
            conversion_goals=["maximize_clicks"]
        )
        
        with patch.object(cli_interface.generator, 'generate_complete_website') as mock_generate:
            mock_result = GeneratedWebsite(
                project_name="test-brand",
                file_structure={
                    "pages/index.tsx": "// Test page",
                    "components/Hero.tsx": "// Test component"
                },
                package_json={"name": "test-brand"},
                vercel_config={"version": 2},
                environment_variables={"API_KEY": "test"}
            )
            mock_generate.return_value = mock_result
            
            # This should complete without errors
            await cli_interface.generate_website_with_streaming(sample_request)
            
            # Verify generation was called
            mock_generate.assert_called_once()
    
    def test_display_generation_results(self, cli_interface):
        """Test result display functionality."""
        mock_result = Mock()
        mock_result.project_name = "test-project"
        mock_result.file_structure = {
            "pages/index.tsx": "// Page content",
            "components/Hero.tsx": "// Component content",
            "package.json": "// Package config"
        }
        mock_result.environment_variables = {
            "API_KEY": "test_key",
            "BRAND_NAME": "Test Brand"
        }
        
        # This should not raise any exceptions
        cli_interface.display_generation_results(mock_result)
    
    def test_handle_error(self, cli_interface):
        """Test error handling display."""
        test_error = Exception("Test error message")
        
        # This should not raise any exceptions
        cli_interface.handle_error(test_error)


class TestMultiAgentInteraction:
    """Test interaction between multiple agents."""
    
    @pytest.fixture
    def research_agent(self):
        """Create research agent."""
        return ResearchAgent()
    
    @pytest.fixture
    def website_generator(self):
        """Create website generator agent."""
        return WebsiteGeneratorAgent()
    
    @pytest.mark.asyncio
    async def test_research_agent_as_tool(self, website_generator, research_agent):
        """Test using research agent as a tool in website generator."""
        deps = AgentDependencies()
        
        # Mock research result
        mock_research_result = ResearchResult(
            query="test query",
            findings=["Research finding 1", "Research finding 2"],
            sources=["https://example.com"],
            recommendations=[
                ConversionElement(
                    element_type="button",
                    psychology_principle="urgency",
                    color_scheme="red",
                    text_content="Act now!",
                    placement="above fold"
                )
            ],
            confidence_score=0.85,
            research_timestamp=asyncio.get_event_loop().time()
        )
        
        with patch.object(website_generator.research_agent, 'quick_research') as mock_research:
            mock_research.return_value = mock_research_result
            
            # Find and test the UI research tool
            ui_research_tool = None
            for tool in website_generator.agent.tools:
                if tool.name == "get_ui_research":
                    ui_research_tool = tool
                    break
            
            assert ui_research_tool is not None
            
            ctx = Mock()
            ctx.deps = deps
            
            result = await ui_research_tool.call(
                ctx=ctx,
                niche="tech",
                focus_area="conversion",
                target_audience="Tech users"
            )
            
            assert isinstance(result, str)
            assert "Research Results" in result
            assert "0.85" in result  # Confidence score
            assert "Research finding 1" in result
            
            # Verify research agent was called correctly
            mock_research.assert_called_once()
            call_args = mock_research.call_args[1]
            assert "conversion best practices for tech affiliate marketing targeting Tech users" in call_args['topic']

    @pytest.mark.asyncio
    async def test_agent_dependency_injection(self, website_generator):
        """Test proper dependency injection between agents."""
        deps = AgentDependencies(
            output_directory="./test_output",
            template_directory="./test_templates"
        )
        
        # Test that dependencies are properly passed through the system
        with patch.object(website_generator.agent, 'run') as mock_run:
            mock_result = Mock()
            mock_result.data = GeneratedWebsite(
                project_name="test",
                file_structure={},
                package_json={},
                vercel_config={},
                environment_variables={}
            )
            mock_run.return_value = mock_result
            
            sample_request = WebsiteGenerationRequest(
                niche=NicheType.GENERAL,
                brand_name="Test",
                target_audience="Test Audience",
                sheets_config=GoogleSheetsConfig(sheet_id="test"),
                color_scheme="blue",
                features=[],
                conversion_goals=[]
            )
            
            await website_generator.generate_complete_website(sample_request, deps)
            
            # Verify dependencies were passed
            call_args = mock_run.call_args
            assert call_args[1]['deps'] == deps


class TestSystemValidation:
    """Test system-wide validation and quality checks."""
    
    @pytest.mark.asyncio
    async def test_generated_website_structure_validation(self):
        """Test that generated websites have the correct structure."""
        settings = Settings()
        generator = WebsiteGeneratorAgent(settings)
        
        sample_request = WebsiteGenerationRequest(
            niche=NicheType.TECH,
            brand_name="Test Brand",
            target_audience="Tech users",
            sheets_config=GoogleSheetsConfig(sheet_id="test_sheet"),
            color_scheme="blue",
            features=["responsive_design", "seo_optimized"],
            conversion_goals=["maximize_clicks"]
        )
        
        # Mock all the dependencies
        with patch.object(generator.file_generator, 'generate_website') as mock_file_gen:
            mock_website = GeneratedWebsite(
                project_name="test-brand",
                file_structure={
                    # Required Next.js structure
                    "pages/index.tsx": "// Home page",
                    "pages/category/[slug].tsx": "// Category page",
                    "pages/api/sheets.ts": "// API route",
                    
                    # Required components
                    "components/ProductCard.tsx": "// Product card",
                    "components/Hero.tsx": "// Hero section",
                    "components/Navigation.tsx": "// Navigation",
                    "components/Footer.tsx": "// Footer",
                    
                    # Configuration files
                    "package.json": json.dumps({"name": "test-brand"}),
                    "tailwind.config.js": "// Tailwind config",
                    "next.config.js": "// Next.js config",
                    "vercel.json": json.dumps({"version": 2})
                },
                package_json={"name": "test-brand"},
                vercel_config={"version": 2},
                environment_variables={
                    "GOOGLE_SHEETS_API_KEY": "test-key",
                    "NEXT_PUBLIC_BRAND_NAME": "Test Brand"
                }
            )
            mock_file_gen.return_value = mock_website
            
            deps = AgentDependencies()
            result = await generator.generate_complete_website(sample_request, deps)
            
            # Validate required files are present
            required_files = [
                "pages/index.tsx",
                "pages/category/[slug].tsx", 
                "pages/api/sheets.ts",
                "components/ProductCard.tsx",
                "components/Hero.tsx",
                "components/Navigation.tsx",
                "components/Footer.tsx",
                "package.json",
                "tailwind.config.js",
                "next.config.js",
                "vercel.json"
            ]
            
            for required_file in required_files:
                assert required_file in result.file_structure, f"Missing required file: {required_file}"
            
            # Validate environment variables
            assert "GOOGLE_SHEETS_API_KEY" in result.environment_variables
            assert "NEXT_PUBLIC_BRAND_NAME" in result.environment_variables
            
            # Validate project structure
            assert result.project_name == "test-brand"
            assert result.package_json["name"] == "test-brand"
            assert result.vercel_config["version"] == 2
    
    def test_configuration_validation(self):
        """Test that system configuration is properly validated."""
        # Test valid configuration
        valid_config = GoogleSheetsConfig(
            sheet_id="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
            range_name="Sheet1!A:G"
        )
        assert valid_config.sheet_id is not None
        assert valid_config.range_name is not None
        
        # Test that NicheType enum works correctly
        assert NicheType.TECH.value == "tech"
        assert NicheType.FASHION.value == "fashion"
        assert NicheType.GENERAL.value == "general"
        
        # Test WebsiteGenerationRequest validation
        request = WebsiteGenerationRequest(
            niche=NicheType.TECH,
            brand_name="Test Brand",
            target_audience="Test Audience",
            sheets_config=valid_config,
            color_scheme="blue",
            features=["responsive_design"],
            conversion_goals=["maximize_clicks"]
        )
        
        assert request.niche == NicheType.TECH
        assert request.brand_name == "Test Brand"
        assert request.sheets_config.sheet_id == valid_config.sheet_id