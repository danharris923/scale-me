"""
Tests for Research Agent.

Comprehensive test suite covering research functionality, web research tools,
and conversion optimization recommendations.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from agents.research_agent import ResearchAgent
from agents.models import (
    ResearchQuery,
    ResearchResult,
    AgentDependencies,
    ConversionElement,
    NicheType
)
from tools.web_research import WebResearchError
from config.settings import Settings


class TestResearchAgent:
    """Test suite for Research Agent."""
    
    @pytest.fixture
    def settings(self):
        """Create test settings."""
        return Settings()
    
    @pytest.fixture
    def agent(self, settings):
        """Create Research Agent instance."""
        return ResearchAgent(settings)
    
    @pytest.fixture
    def sample_deps(self):
        """Create sample agent dependencies."""
        return AgentDependencies()
    
    @pytest.fixture
    def sample_research_result(self):
        """Create sample research result."""
        recommendations = [
            ConversionElement(
                element_type="button",
                psychology_principle="urgency",
                color_scheme="red for action",
                text_content="Buy Now - Limited Time!",
                placement="above the fold"
            )
        ]
        
        return ResearchResult(
            query="conversion optimization for tech",
            findings=["Finding 1", "Finding 2"],
            sources=["https://example.com"],
            recommendations=recommendations,
            confidence_score=0.85,
            research_timestamp=datetime.now()
        )
    
    def test_agent_initialization(self, settings):
        """Test that research agent initializes correctly."""
        agent = ResearchAgent(settings)
        
        assert agent.settings == settings
        assert agent.provider is not None
        assert agent.web_research_tool is not None
        assert agent.agent is not None
    
    def test_agent_initialization_with_defaults(self):
        """Test that agent initializes with default settings."""
        agent = ResearchAgent()
        
        assert agent.settings is not None
        assert isinstance(agent.settings, Settings)
    
    def test_system_prompt_generation(self, agent):
        """Test that system prompt contains required elements."""
        system_prompt = agent._get_system_prompt()
        
        assert isinstance(system_prompt, str)
        assert len(system_prompt) > 500
        assert "conversion psychology" in system_prompt
        assert "UI/UX" in system_prompt
        assert "Tailwind CSS" in system_prompt
        assert "accessibility" in system_prompt
        assert "mobile-first" in system_prompt
        assert "evidence-based recommendations" in system_prompt
    
    @pytest.mark.asyncio
    async def test_research_conversion_techniques_tool(self, agent, sample_deps, sample_research_result):
        """Test the research conversion techniques tool."""
        with patch.object(agent.web_research_tool, 'research') as mock_research:
            mock_research.return_value = sample_research_result
            
            # Find the research tool
            research_tool = None
            for tool in agent.agent.tools:
                if tool.name == "research_conversion_techniques":
                    research_tool = tool
                    break
            
            assert research_tool is not None
            
            ctx = Mock()
            ctx.deps = sample_deps
            
            result = await research_tool.call(
                ctx=ctx,
                topic="button design for CTAs",
                niche="tech",
                focus_area="conversion",
                max_sources=3
            )
            
            assert isinstance(result, str)
            assert "Research Results" in result
            assert "Confidence Score: 0.85" in result
            assert "Finding 1" in result
            assert "Finding 2" in result
            assert "urgency" in result
            assert "red for action" in result
            
            # Verify research tool was called with correct parameters
            mock_research.assert_called_once()
            call_args = mock_research.call_args[0][0]  # First positional argument (ResearchQuery)
            assert call_args.topic == "button design for CTAs for tech affiliate marketing"
            assert call_args.focus_area == "conversion"
            assert call_args.niche_context == NicheType.TECH
            assert call_args.max_sources == 3
    
    @pytest.mark.asyncio
    async def test_research_tool_with_web_research_error(self, agent, sample_deps):
        """Test research tool handling of web research errors."""
        with patch.object(agent.web_research_tool, 'research') as mock_research:
            mock_research.side_effect = WebResearchError("Network error")
            
            research_tool = None
            for tool in agent.agent.tools:
                if tool.name == "research_conversion_techniques":
                    research_tool = tool
                    break
            
            ctx = Mock()
            ctx.deps = sample_deps
            
            result = await research_tool.call(
                ctx=ctx,
                topic="test topic",
                niche="tech",
                focus_area="conversion",
                max_sources=3
            )
            
            assert isinstance(result, str)
            assert "Research failed: Network error" in result
            assert "Using fallback knowledge" in result
    
    @pytest.mark.asyncio
    async def test_analyze_competition_tool(self, agent, sample_deps, sample_research_result):
        """Test the competition analysis tool."""
        with patch.object(agent.web_research_tool, 'research') as mock_research:
            mock_research.return_value = sample_research_result
            
            # Find the competition analysis tool
            competition_tool = None
            for tool in agent.agent.tools:
                if tool.name == "analyze_competition":
                    competition_tool = tool
                    break
            
            assert competition_tool is not None
            
            ctx = Mock()
            ctx.deps = sample_deps
            
            result = await competition_tool.call(
                ctx=ctx,
                niche="tech",
                competitors=["https://competitor1.com", "https://competitor2.com"],
                focus_areas=["ui_ux", "conversion"]
            )
            
            assert isinstance(result, str)
            assert "Competitive Analysis for tech Niche" in result
            assert "UI_UX Analysis" in result
            assert "CONVERSION Analysis" in result
            assert "Recommendations" in result
            
            # Verify research was called for each focus area
            assert mock_research.call_count == 2
    
    @pytest.mark.asyncio
    async def test_get_niche_insights_tool(self, agent, sample_deps, sample_research_result):
        """Test the niche insights tool."""
        with patch.object(agent.web_research_tool, 'research') as mock_research:
            mock_research.return_value = sample_research_result
            
            # Find the niche insights tool
            insights_tool = None
            for tool in agent.agent.tools:
                if tool.name == "get_niche_insights":
                    insights_tool = tool
                    break
            
            assert insights_tool is not None
            
            ctx = Mock()
            ctx.deps = sample_deps
            
            result = await insights_tool.call(
                ctx=ctx,
                niche="fashion",
                target_audience="young professionals",
                conversion_goals=["maximize_clicks", "build_trust"]
            )
            
            assert isinstance(result, str)
            assert "Niche Insights for fashion" in result
            assert "young professionals" in result
            assert "Maximize Clicks" in result
            assert "Build Trust" in result
            
            # Verify research was called for each conversion goal
            assert mock_research.call_count == 2
    
    @pytest.mark.asyncio
    async def test_research_performance_optimization_tool(self, agent, sample_deps, sample_research_result):
        """Test the performance optimization research tool."""
        with patch.object(agent.web_research_tool, 'research') as mock_research:
            mock_research.return_value = sample_research_result
            
            # Find the performance research tool
            perf_tool = None
            for tool in agent.agent.tools:
                if tool.name == "research_performance_optimization":
                    perf_tool = tool
                    break
            
            assert perf_tool is not None
            
            ctx = Mock()
            ctx.deps = sample_deps
            
            current_performance = {
                "lighthouse_score": 75.0,
                "lcp": 3500.0,
                "cls": 0.15
            }
            
            target_metrics = {
                "lighthouse_score": 90.0,
                "lcp": 2500.0,
                "cls": 0.1
            }
            
            result = await perf_tool.call(
                ctx=ctx,
                website_type="affiliate_marketing",
                current_performance=current_performance,
                target_metrics=target_metrics
            )
            
            assert isinstance(result, str)
            assert "Performance Optimization Research" in result
            assert "affiliate_marketing" in result
            assert "Current vs Target Metrics" in result
            assert "lighthouse_score: 75.0 → 90.0" in result
            assert "⚠️ Needs Improvement" in result
            
            # Verify research was called with performance focus
            mock_research.assert_called_once()
            call_args = mock_research.call_args[0][0]
            assert call_args.focus_area == "performance"
    
    @pytest.mark.asyncio
    async def test_conduct_comprehensive_research(self, agent, sample_deps):
        """Test comprehensive research functionality."""
        with patch.object(agent.agent, 'run') as mock_run:
            mock_result = Mock()
            mock_result.data = sample_research_result
            mock_run.return_value = mock_result
            
            result = await agent.conduct_comprehensive_research(
                niche="tech",
                target_audience="tech enthusiasts",
                conversion_goals=["maximize_clicks"],
                deps=sample_deps
            )
            
            assert isinstance(result, ResearchResult)
            
            # Verify agent was called with comprehensive prompt
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            prompt = call_args[0][0]
            assert "tech" in prompt
            assert "tech enthusiasts" in prompt
            assert "maximize_clicks" in prompt
            assert "conversion optimization techniques" in prompt
    
    @pytest.mark.asyncio
    async def test_quick_research(self, agent):
        """Test quick research functionality."""
        with patch.object(agent.agent, 'run') as mock_run:
            mock_result = Mock()
            mock_result.data = sample_research_result
            mock_run.return_value = mock_result
            
            result = await agent.quick_research(
                topic="mobile optimization",
                niche="fashion",
                focus_area="ui_ux"
            )
            
            assert isinstance(result, ResearchResult)
            
            # Verify agent was called with quick research prompt
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            prompt = call_args[0][0]
            assert "mobile optimization" in prompt
            assert "fashion" in prompt
            assert "ui_ux" in prompt
    
    @pytest.mark.asyncio
    async def test_quick_research_with_custom_deps(self, agent, sample_deps):
        """Test quick research with custom dependencies."""
        with patch.object(agent.agent, 'run') as mock_run:
            mock_result = Mock()
            mock_result.data = sample_research_result
            mock_run.return_value = mock_result
            
            result = await agent.quick_research(
                topic="color psychology",
                deps=sample_deps
            )
            
            assert isinstance(result, ResearchResult)
            
            # Verify custom deps were used
            call_args = mock_run.call_args
            assert call_args[1]['deps'] == sample_deps
    
    def test_tool_registration(self, agent):
        """Test that all required tools are registered."""
        tool_names = [tool.name for tool in agent.agent.tools]
        
        expected_tools = [
            "research_conversion_techniques",
            "analyze_competition",
            "get_niche_insights",
            "research_performance_optimization"
        ]
        
        for expected_tool in expected_tools:
            assert expected_tool in tool_names
    
    @pytest.mark.asyncio
    async def test_niche_type_handling_in_tools(self, agent, sample_deps, sample_research_result):
        """Test proper niche type handling in tools."""
        with patch.object(agent.web_research_tool, 'research') as mock_research:
            mock_research.return_value = sample_research_result
            
            research_tool = None
            for tool in agent.agent.tools:
                if tool.name == "research_conversion_techniques":
                    research_tool = tool
                    break
            
            ctx = Mock()
            ctx.deps = sample_deps
            
            # Test with valid niche
            await research_tool.call(
                ctx=ctx,
                topic="test",
                niche="fashion",
                focus_area="conversion"
            )
            
            call_args = mock_research.call_args[0][0]
            assert call_args.niche_context == NicheType.FASHION
            
            # Test with invalid niche - should default to GENERAL
            await research_tool.call(
                ctx=ctx,
                topic="test",
                niche="invalid_niche",
                focus_area="conversion"
            )
            
            call_args = mock_research.call_args[0][0]
            assert call_args.niche_context == NicheType.GENERAL
    
    @pytest.mark.asyncio
    async def test_error_handling_in_comprehensive_research(self, agent, sample_deps):
        """Test error handling in comprehensive research."""
        with patch.object(agent.agent, 'run') as mock_run:
            mock_run.side_effect = Exception("Test error")
            
            with pytest.raises(Exception) as exc_info:
                await agent.conduct_comprehensive_research(
                    niche="tech",
                    target_audience="test",
                    conversion_goals=["test"],
                    deps=sample_deps
                )
            
            assert "Test error" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_error_handling_in_quick_research(self, agent):
        """Test error handling in quick research."""
        with patch.object(agent.agent, 'run') as mock_run:
            mock_run.side_effect = Exception("Quick research error")
            
            with pytest.raises(Exception) as exc_info:
                await agent.quick_research(topic="test topic")
            
            assert "Quick research error" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_tool_error_handling_with_generic_exception(self, agent, sample_deps):
        """Test tool error handling with generic exceptions."""
        with patch.object(agent.web_research_tool, 'research') as mock_research:
            mock_research.side_effect = Exception("Generic error")
            
            research_tool = None
            for tool in agent.agent.tools:
                if tool.name == "research_conversion_techniques":
                    research_tool = tool
                    break
            
            ctx = Mock()
            ctx.deps = sample_deps
            
            result = await research_tool.call(
                ctx=ctx,
                topic="test",
                niche="tech",
                focus_area="conversion"
            )
            
            assert isinstance(result, str)
            assert "Error occurred during research" in result
            assert "Please try again" in result
    
    @pytest.fixture
    def sample_research_result(self):
        """Create sample research result with proper structure."""
        recommendations = [
            ConversionElement(
                element_type="button",
                psychology_principle="urgency",
                color_scheme="red for action",
                text_content="Buy Now - Limited Time! This is a longer text that should be truncated in the output for better display.",
                placement="above the fold"
            )
        ]
        
        return ResearchResult(
            query="conversion optimization for tech",
            findings=["Finding 1: Important insight", "Finding 2: Another insight"],
            sources=["https://example.com", "https://test.com"],
            recommendations=recommendations,
            confidence_score=0.85,
            research_timestamp=datetime.now()
        )
    
    @pytest.mark.asyncio
    async def test_research_output_formatting(self, agent, sample_deps, sample_research_result):
        """Test that research output is properly formatted."""
        with patch.object(agent.web_research_tool, 'research') as mock_research:
            mock_research.return_value = sample_research_result
            
            research_tool = None
            for tool in agent.agent.tools:
                if tool.name == "research_conversion_techniques":
                    research_tool = tool
                    break
            
            ctx = Mock()
            ctx.deps = sample_deps
            
            result = await research_tool.call(
                ctx=ctx,
                topic="button design",
                niche="tech",
                focus_area="conversion"
            )
            
            # Verify proper formatting
            assert "Research Results - CONVERSION for tech:" in result
            assert "Confidence Score: 0.85" in result
            assert "Key Findings:" in result
            assert "1. Finding 1: Important insight" in result
            assert "2. Finding 2: Another insight" in result
            assert "Conversion Recommendations:" in result
            assert "1. Button - urgency" in result
            assert "Color Strategy: red for action" in result
            assert "Placement: above the fold" in result
            assert "Example: Buy Now - Limited Time! This is a longer text that should be truncated in the output for" in result