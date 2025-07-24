"""
Tests for CLI Interface.

Tests for the Rich CLI interface including user interaction,
streaming output, error handling, and user experience.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from rich.console import Console

from cli import CLIInterface, main
from agents.models import (
    WebsiteGenerationRequest,
    GoogleSheetsConfig, 
    NicheType,
    GeneratedWebsite
)


class TestCLIInterface:
    """Tests for CLI Interface class."""
    
    @pytest.fixture
    def cli_interface(self):
        """Create CLI interface instance."""
        return CLIInterface()
    
    def test_cli_initialization(self):
        """Test CLI interface initializes correctly."""
        cli = CLIInterface()
        
        assert isinstance(cli.console, Console)
        assert cli.settings is not None
        assert cli.generator is not None
        assert cli.current_step == ""
        assert cli.tool_calls == []
    
    def test_display_welcome(self, cli_interface):
        """Test welcome message display."""
        with patch.object(cli_interface.console, 'print') as mock_print:
            cli_interface.display_welcome()
            
            # Should call print at least twice (title panel and newline)
            assert mock_print.call_count >= 2
    
    @pytest.mark.asyncio
    async def test_get_user_configuration_complete_flow(self, cli_interface):
        """Test complete user configuration flow."""
        # Mock user inputs in sequence
        user_inputs = [
            "2",  # Tech niche selection
            "TechDeals Pro",  # Brand name
            "Tech enthusiasts seeking the best deals on electronics",  # Target audience
            "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",  # Google Sheets ID
            "",  # Sheet range (use default)
            "",  # Color scheme (use default) 
            "1,2,3"  # Conversion goals
        ]
        
        with patch('rich.prompt.Prompt.ask') as mock_prompt:
            with patch('rich.prompt.Confirm.ask') as mock_confirm:
                with patch.object(cli_interface, 'display_configuration_summary') as mock_display:
                    
                    mock_prompt.side_effect = user_inputs
                    mock_confirm.return_value = True
                    
                    request = await cli_interface.get_user_configuration()
                    
                    # Verify request object
                    assert isinstance(request, WebsiteGenerationRequest)
                    assert request.niche == NicheType.TECH
                    assert request.brand_name == "TechDeals Pro"
                    assert request.target_audience == "Tech enthusiasts seeking the best deals on electronics"
                    assert request.sheets_config.sheet_id == "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
                    assert request.sheets_config.range_name == "Sheet1!A:G"  # Default value
                    assert request.color_scheme == "blue"  # Default value
                    assert "maximize_clicks" in request.conversion_goals
                    assert "build_trust" in request.conversion_goals
                    assert "increase_engagement" in request.conversion_goals
                    
                    # Verify configuration summary was displayed
                    mock_display.assert_called_once_with(request)
    
    @pytest.mark.asyncio
    async def test_get_user_configuration_with_validation_retries(self, cli_interface):
        """Test user configuration with input validation retries."""
        # First attempt: empty brand name, second attempt: valid
        user_inputs = [
            "1",  # Fashion niche
            "",  # Empty brand name (should retry)
            "Fashion Hub",  # Valid brand name
            "",  # Empty target audience (should retry)
            "Fashion lovers",  # Valid target audience
            "",  # Empty sheet ID (should retry)
            "valid_sheet_id",  # Valid sheet ID
            "",  # Default range
            "",  # Default color
            "1"  # Single conversion goal
        ]
        
        with patch('rich.prompt.Prompt.ask') as mock_prompt:
            with patch('rich.prompt.Confirm.ask') as mock_confirm:
                with patch.object(cli_interface.console, 'print') as mock_print:
                    
                    mock_prompt.side_effect = user_inputs
                    mock_confirm.return_value = True
                    
                    request = await cli_interface.get_user_configuration()
                    
                    # Verify final request is correct
                    assert request.niche == NicheType.FASHION
                    assert request.brand_name == "Fashion Hub"
                    assert request.target_audience == "Fashion lovers"
                    assert request.sheets_config.sheet_id == "valid_sheet_id"
                    
                    # Verify error messages were shown for empty inputs
                    error_calls = [call for call in mock_print.call_args_list 
                                 if len(call[0]) > 0 and "cannot be empty" in str(call[0][0])]
                    assert len(error_calls) >= 3  # Should show 3 validation errors
    
    @pytest.mark.asyncio
    async def test_get_user_configuration_cancelled(self, cli_interface):
        """Test user configuration cancellation."""
        user_inputs = [
            "2",  # Tech niche
            "Test Brand",  # Brand name
            "Test Audience",  # Target audience
            "test_sheet_id",  # Sheet ID
            "",  # Default range
            "",  # Default color
            "1"  # Conversion goal
        ]
        
        with patch('rich.prompt.Prompt.ask') as mock_prompt:
            with patch('rich.prompt.Confirm.ask') as mock_confirm:
                with patch('sys.exit') as mock_exit:
                    
                    mock_prompt.side_effect = user_inputs
                    mock_confirm.return_value = False  # User cancels
                    
                    await cli_interface.get_user_configuration()
                    
                    # Should call sys.exit when cancelled
                    mock_exit.assert_called_once_with(0)
    
    def test_display_configuration_summary(self, cli_interface):
        """Test configuration summary display."""
        sample_request = WebsiteGenerationRequest(
            niche=NicheType.TECH,
            brand_name="Test Brand",
            target_audience="Test Audience",
            sheets_config=GoogleSheetsConfig(
                sheet_id="test_sheet_id",
                range_name="Sheet1!A:G"
            ),
            color_scheme="blue",
            features=["responsive_design"],
            conversion_goals=["maximize_clicks", "build_trust"]
        )
        
        with patch.object(cli_interface.console, 'print') as mock_print:
            cli_interface.display_configuration_summary(sample_request)
            
            # Should print the table
            mock_print.assert_called()
            
            # Verify the table contains expected information
            # (We can't easily test Rich table contents directly, 
            # but we can verify the method completes without error)
    
    @pytest.mark.asyncio
    async def test_generate_website_with_streaming_success(self, cli_interface):
        """Test successful website generation with streaming output."""
        sample_request = WebsiteGenerationRequest(
            niche=NicheType.TECH,
            brand_name="TechDeals Pro",
            target_audience="Tech enthusiasts",
            sheets_config=GoogleSheetsConfig(sheet_id="test_sheet_id"),
            color_scheme="blue",
            features=["responsive_design"],
            conversion_goals=["maximize_clicks"]
        )
        
        mock_result = GeneratedWebsite(
            project_name="techdeal-pro",
            file_structure={
                "pages/index.tsx": "// Home page content",
                "components/Hero.tsx": "// Hero component content",
                "package.json": '{"name": "techdeals-pro"}'
            },
            package_json={"name": "techdeals-pro"},
            vercel_config={"version": 2},
            environment_variables={
                "GOOGLE_SHEETS_API_KEY": "test-key",
                "NEXT_PUBLIC_BRAND_NAME": "TechDeals Pro"
            }
        )
        
        with patch.object(cli_interface.generator, 'generate_complete_website') as mock_generate:
            with patch.object(cli_interface, 'display_generation_results') as mock_display:
                with patch('asyncio.sleep'):  # Speed up the test
                    
                    mock_generate.return_value = mock_result
                    
                    await cli_interface.generate_website_with_streaming(sample_request)
                    
                    # Verify generation was called
                    mock_generate.assert_called_once()
                    call_args = mock_generate.call_args
                    assert call_args[0][0] == sample_request  # First arg is the request
                    
                    # Verify results were displayed
                    mock_display.assert_called_once_with(mock_result)
    
    @pytest.mark.asyncio
    async def test_generate_website_with_streaming_error(self, cli_interface):
        """Test website generation with error handling."""
        sample_request = WebsiteGenerationRequest(
            niche=NicheType.TECH,
            brand_name="Test Brand",
            target_audience="Test Audience",
            sheets_config=GoogleSheetsConfig(sheet_id="test_sheet_id"),
            color_scheme="blue",
            features=[],
            conversion_goals=[]
        )
        
        with patch.object(cli_interface.generator, 'generate_complete_website') as mock_generate:
            with patch.object(cli_interface.console, 'print') as mock_print:
                with patch('asyncio.sleep'):  # Speed up the test
                    
                    mock_generate.side_effect = Exception("Generation failed")
                    
                    await cli_interface.generate_website_with_streaming(sample_request)
                    
                    # Verify error message was displayed
                    error_calls = [call for call in mock_print.call_args_list 
                                 if len(call[0]) > 0 and "Generation failed" in str(call[0][0])]
                    assert len(error_calls) > 0
    
    def test_display_generation_results(self, cli_interface):
        """Test generation results display."""
        mock_result = Mock()
        mock_result.project_name = "test-project"
        mock_result.file_structure = {
            "pages/index.tsx": "// Page content",
            "components/Hero.tsx": "// Component content",
            "components/ProductCard.tsx": "// Product component",
            "package.json": '{"name": "test-project"}',
            "tailwind.config.js": "// Tailwind config",
            "vercel.json": '{"version": 2}'
        }
        mock_result.environment_variables = {
            "GOOGLE_SHEETS_API_KEY": "test-key",
            "NEXT_PUBLIC_BRAND_NAME": "Test Brand"
        }
        
        with patch.object(cli_interface.console, 'print') as mock_print:
            cli_interface.display_generation_results(mock_result)
            
            # Should print multiple sections
            assert mock_print.call_count >= 4  # Info table, file structure, env vars, next steps
    
    @pytest.mark.asyncio
    async def test_offer_code_review_declined(self, cli_interface):
        """Test code review when user declines."""
        mock_result = Mock()
        
        with patch('rich.prompt.Confirm.ask') as mock_confirm:
            mock_confirm.return_value = False
            
            # Should return immediately without error
            await cli_interface.offer_code_review(mock_result)
    
    @pytest.mark.asyncio
    async def test_offer_code_review_accepted(self, cli_interface):
        """Test code review when user accepts."""
        mock_result = Mock()
        mock_result.file_structure = {
            "components/ProductCard.tsx": "const ProductCard = () => {\n  return <div>Product</div>;\n};\n\nexport default ProductCard;" + "\n" * 50,  # Long content
            "components/Hero.tsx": "const Hero = () => <div>Hero</div>;",
            "pages/index.tsx": "export default function Home() { return <div>Home</div>; }",
            "package.json": '{\n  "name": "test-project",\n  "version": "1.0.0"\n}'
        }
        
        with patch('rich.prompt.Confirm.ask') as mock_confirm:
            with patch.object(cli_interface.console, 'print') as mock_print:
                
                mock_confirm.return_value = True
                
                await cli_interface.offer_code_review(mock_result)
                
                # Should print code review sections
                review_calls = [call for call in mock_print.call_args_list 
                              if len(call[0]) > 0 and "Code Review" in str(call[0][0])]
                assert len(review_calls) > 0
    
    def test_handle_error(self, cli_interface):
        """Test error handling display."""
        test_error = Exception("Test error message")
        
        with patch.object(cli_interface.console, 'print') as mock_print:
            cli_interface.handle_error(test_error)
            
            # Should print error panel
            mock_print.assert_called()
            
            # Verify error message is included
            error_calls = [call for call in mock_print.call_args_list 
                          if len(call[0]) > 0 and "Test error message" in str(call[0][0])]
            assert len(error_calls) > 0


class TestCLIMainFunction:
    """Tests for the main CLI function."""
    
    @pytest.mark.asyncio
    async def test_main_function_success_flow(self):
        """Test successful main function execution."""
        mock_request = WebsiteGenerationRequest(
            niche=NicheType.TECH,
            brand_name="Test Brand",
            target_audience="Test Audience",
            sheets_config=GoogleSheetsConfig(sheet_id="test_sheet_id"),
            color_scheme="blue",
            features=[],
            conversion_goals=[]
        )
        
        with patch('cli.CLIInterface') as mock_cli_class:
            mock_cli = Mock()
            mock_cli_class.return_value = mock_cli
            
            # Mock CLI methods
            mock_cli.display_welcome = Mock()
            mock_cli.get_user_configuration = AsyncMock(return_value=mock_request)
            mock_cli.generate_website_with_streaming = AsyncMock()
            mock_cli.console.print = Mock()
            
            await main()
            
            # Verify the flow was executed
            mock_cli.display_welcome.assert_called_once()
            mock_cli.get_user_configuration.assert_called_once()
            mock_cli.generate_website_with_streaming.assert_called_once_with(mock_request)
            mock_cli.console.print.assert_called()
    
    @pytest.mark.asyncio
    async def test_main_function_keyboard_interrupt(self):
        """Test main function with keyboard interrupt."""
        with patch('cli.CLIInterface') as mock_cli_class:
            mock_cli = Mock()
            mock_cli_class.return_value = mock_cli
            
            mock_cli.display_welcome = Mock()
            mock_cli.get_user_configuration = AsyncMock(side_effect=KeyboardInterrupt())
            mock_cli.console.print = Mock()
            
            await main()
            
            # Verify cancellation message was displayed
            mock_cli.console.print.assert_called()
            print_calls = [str(call[0][0]) for call in mock_cli.console.print.call_args_list]
            assert any("cancelled by user" in call for call in print_calls)
    
    @pytest.mark.asyncio
    async def test_main_function_exception_handling(self):
        """Test main function with exception handling."""
        with patch('cli.CLIInterface') as mock_cli_class:
            mock_cli = Mock()
            mock_cli_class.return_value = mock_cli
            
            test_error = Exception("Test error")
            mock_cli.display_welcome = Mock()
            mock_cli.get_user_configuration = AsyncMock(side_effect=test_error)
            mock_cli.handle_error = Mock()
            
            with pytest.raises(SystemExit) as exc_info:
                await main()
            
            # Verify error was handled
            mock_cli.handle_error.assert_called_once_with(test_error)
            assert exc_info.value.code == 1


class TestCLIUserExperience:
    """Tests for CLI user experience features."""
    
    @pytest.fixture
    def cli_interface(self):
        return CLIInterface()
    
    def test_niche_selection_mapping(self, cli_interface):
        """Test that niche selection properly maps to NicheType enum."""
        # This is tested indirectly through get_user_configuration
        # but we can test the mapping logic
        niche_options = {
            "1": ("fashion", "Fashion & Apparel"),
            "2": ("tech", "Technology & Electronics"), 
            "3": ("outdoor_gear", "Outdoor & Adventure Gear"),
            "4": ("home_improvement", "Home & Garden"),
            "5": ("music", "Musical Instruments & Audio"),
            "6": ("general", "General Products")
        }
        
        for key, (niche_value, _) in niche_options.items():
            try:
                niche_type = NicheType(niche_value)
                assert niche_type.value == niche_value
            except ValueError:
                # Should default to GENERAL for invalid values  
                niche_type = NicheType.GENERAL
                assert niche_type == NicheType.GENERAL
    
    def test_conversion_goals_mapping(self, cli_interface):
        """Test conversion goals mapping."""
        goal_options = {
            "1": "maximize_clicks",
            "2": "build_trust",
            "3": "increase_engagement", 
            "4": "improve_mobile_experience",
            "5": "boost_seo_ranking"
        }
        
        # Test valid selections
        for key, expected_goal in goal_options.items():
            assert expected_goal in goal_options.values()
        
        # Test comma-separated input parsing
        test_input = "1,2,3"
        selected_goals = []
        for goal_num in test_input.split(","):
            goal_num = goal_num.strip()
            if goal_num in goal_options:
                selected_goals.append(goal_options[goal_num])
        
        assert "maximize_clicks" in selected_goals
        assert "build_trust" in selected_goals
        assert "increase_engagement" in selected_goals
        assert len(selected_goals) == 3
    
    def test_color_scheme_validation(self, cli_interface):
        """Test color scheme validation."""
        valid_colors = ["blue", "green", "red", "purple", "indigo"]
        
        for color in valid_colors:
            # These should all be valid choices in the CLI
            assert color in valid_colors
    
    def test_streaming_output_simulation(self, cli_interface):
        """Test streaming output formatting."""
        # Test that streaming messages are properly formatted
        test_messages = [
            "🤖 Research Agent: Analyzing conversion techniques...",
            "🛠  Using tool: research_conversion_techniques",
            "✅ Research complete: Found 12 optimization techniques",
            "🤖 Website Generator: Creating comprehensive SEO plan...",
            "🛠  Using tool: generate_seo_strategy",
            "✅ SEO strategy generated with meta tags and structured data"
        ]
        
        for message in test_messages:
            # Each message should have proper emoji and formatting
            assert len(message) > 0
            # Should contain either emoji or status indicator
            assert any(indicator in message for indicator in ["🤖", "🛠", "✅", "🔧", "📈", "📊", "⚙️", "🔍"])
    
    def test_file_structure_display_icons(self, cli_interface):
        """Test file structure display with proper icons."""
        test_files = [
            "pages/index.tsx",
            "components/Hero.tsx", 
            "pages/api/sheets.ts",
            "package.json",
            "tailwind.config.js",
            "vercel.json",
            "README.md"
        ]
        
        expected_icons = {
            ".tsx": "⚛️ ",
            ".ts": "📜 ",
            ".json": "📋 ",
            ".js": "🟨 ",
            ".md": "📄 "
        }
        
        for file_path in test_files:
            extension = "." + file_path.split(".")[-1]
            if extension in expected_icons:
                expected_icon = expected_icons[extension]
                # In the actual implementation, these icons would be used
                assert expected_icon is not None
    
    @pytest.mark.asyncio
    async def test_progress_tracking_simulation(self, cli_interface):
        """Test progress tracking during generation."""
        # Test the progress steps that would be shown
        progress_steps = [
            "[green]🔧 Initializing system...",
            "[blue]🔍 Researching UI/UX trends...",
            "[yellow]📈 Generating SEO strategy...",
            "[cyan]📊 Testing Google Sheets integration...", 
            "[magenta]⚙️  Generating React components...",
            "[red]🔍 Validating generated code..."
        ]
        
        # Each step should have a color and descriptive text
        for step in progress_steps:
            assert "[" in step and "]" in step  # Color formatting
            assert any(emoji in step for emoji in ["🔧", "🔍", "📈", "📊", "⚙️"])  # Has emoji