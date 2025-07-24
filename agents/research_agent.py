"""
Research Agent specialized in UI/UX and conversion optimization research.

This agent uses the WebResearchTool to gather the latest trends, best practices,
and proven techniques for creating high-converting affiliate marketing websites.
"""

import logging
from typing import List, Dict, Any, Optional
import asyncio

from pydantic_ai import Agent, RunContext
from pydantic_ai.models import Model

from .models import (
    ResearchQuery, 
    ResearchResult, 
    AgentDependencies, 
    ConversionElement,
    NicheType
)
from .providers import LLMProvider
from tools.web_research import WebResearchTool, WebResearchError
from config import Settings

logger = logging.getLogger(__name__)


class ResearchAgent:
    """Agent specialized in UI/UX and conversion optimization research."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.provider = LLMProvider(self.settings)
        self.web_research_tool = WebResearchTool(self.settings)
        
        # Create the agent with enhanced system prompt
        self.agent = self.provider.create_agent_with_fallback(
            system_prompt=self._get_system_prompt(),
            deps_type=AgentDependencies,
            output_type=ResearchResult
        )
        
        # Register tools
        self._register_tools()
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the research agent."""
        return """You are a world-class UI/UX and conversion optimization research specialist with deep expertise in:

**Core Expertise Areas:**
- Conversion psychology and user behavior patterns
- Mobile-first responsive design principles
- Color psychology and trust signal implementation
- Latest Tailwind CSS component patterns and best practices
- Performance optimization techniques for web applications
- Accessibility standards (WCAG 2.1) and inclusive design
- SEO optimization strategies for affiliate marketing

**Research Focus:**
Your primary mission is to research and provide actionable insights for creating high-converting affiliate marketing websites. You excel at:

1. **Conversion Optimization:**
   - Analyzing psychological triggers that drive user actions
   - Identifying optimal CTA placement and design patterns
   - Understanding urgency and scarcity tactics that convert
   - Researching social proof and trust building techniques

2. **UI/UX Best Practices:**
   - Mobile-first design strategies that maximize engagement
   - Navigation patterns that reduce bounce rates
   - Visual hierarchy techniques for conversion funnels
   - User flow optimization for affiliate link engagement

3. **Technical Implementation:**
   - Latest Tailwind CSS utility patterns and components
   - Performance optimization for Core Web Vitals
   - Accessibility compliance strategies
   - SEO-friendly markup and structured data

**Output Standards:**
- Always provide specific, actionable recommendations
- Include confidence scores based on research quality
- Reference credible sources and recent studies
- Focus on measurable conversion improvements
- Consider mobile-first and accessibility requirements

**Approach:**
1. Conduct thorough research using multiple reliable sources
2. Synthesize findings into practical conversion elements
3. Provide context-aware recommendations based on niche
4. Include implementation guidance with code examples when relevant
5. Assess research quality and provide confidence scores

Remember: Your insights directly impact the conversion rates and success of affiliate marketing websites. Prioritize evidence-based recommendations that have proven track records in e-commerce and affiliate marketing contexts."""

    def _register_tools(self) -> None:
        """Register tools for the research agent."""
        
        @self.agent.tool
        async def research_conversion_techniques(
            ctx: RunContext[AgentDependencies],
            topic: str,
            niche: str,
            focus_area: str,
            max_sources: int = 5
        ) -> str:
            """Research the latest conversion optimization techniques for a specific topic and niche.
            
            Args:
                topic: The specific research topic (e.g., "button design for CTAs")
                niche: The business niche context (e.g., "fashion", "tech", "outdoor_gear")
                focus_area: Research focus ("ui_ux", "conversion", "seo", "performance", "accessibility")
                max_sources: Maximum number of sources to research (default: 5)
                
            Returns:
                Synthesized research findings with actionable insights
            """
            try:
                # Map niche string to NicheType
                niche_type = None
                try:
                    niche_type = NicheType(niche.lower().replace(' ', '_'))
                except ValueError:
                    niche_type = NicheType.GENERAL
                
                # Create research query
                query = ResearchQuery(
                    topic=f"{topic} for {niche} affiliate marketing",
                    focus_area=focus_area,
                    niche_context=niche_type,
                    max_sources=max_sources,
                    recency_days=365
                )
                
                # Perform research
                result = await self.web_research_tool.research(query)
                
                # Format findings for the agent
                findings_text = f"Research Results for '{topic}' in {niche} niche:\\n\\n"
                findings_text += f"Confidence Score: {result.confidence_score:.2f}\\n\\n"
                
                findings_text += "Key Findings:\\n"
                for i, finding in enumerate(result.findings, 1):
                    findings_text += f"{i}. {finding}\\n"
                
                findings_text += "\\nConversion Recommendations:\\n"
                for i, rec in enumerate(result.recommendations, 1):
                    findings_text += f"{i}. {rec.element_type.title()} - {rec.psychology_principle}\\n"
                    findings_text += f"   Colors: {rec.color_scheme}\\n"
                    findings_text += f"   Placement: {rec.placement}\\n"
                    findings_text += f"   Example: {rec.text_content[:100]}...\\n\\n"
                
                findings_text += f"\\nSources Researched: {len(result.sources)}\\n"
                findings_text += f"Research Timestamp: {result.research_timestamp}\\n"
                
                return findings_text
                
            except WebResearchError as e:
                logger.error(f"Web research failed: {e}")
                return f"Research failed: {e}. Using fallback knowledge for {topic} in {niche} niche."
            except Exception as e:
                logger.error(f"Unexpected error in research tool: {e}")
                return f"Error occurred during research. Please try again with a different topic or niche."
        
        @self.agent.tool
        async def analyze_competition(
            ctx: RunContext[AgentDependencies],
            niche: str,
            competitors: List[str],
            focus_areas: List[str]
        ) -> str:
            """Analyze competitor websites for conversion optimization insights.
            
            Args:
                niche: The business niche (e.g., "fashion", "tech")
                competitors: List of competitor URLs to analyze
                focus_areas: Areas to focus on (e.g., ["ui_ux", "conversion"])
                
            Returns:
                Competitive analysis with actionable insights
            """
            try:
                analysis_results = []
                
                for focus_area in focus_areas:
                    # Research general patterns in this niche
                    query = ResearchQuery(
                        topic=f"best practices {niche} affiliate websites",
                        focus_area=focus_area,
                        niche_context=NicheType(niche.lower().replace(' ', '_')) if niche in ['fashion', 'tech', 'outdoor_gear'] else NicheType.GENERAL,
                        max_sources=3,
                        recency_days=180
                    )
                    
                    result = await self.web_research_tool.research(query)
                    analysis_results.append({
                        'focus_area': focus_area,
                        'findings': result.findings,
                        'recommendations': result.recommendations
                    })
                
                # Format analysis
                analysis_text = f"Competitive Analysis for {niche} Niche:\\n\\n"
                
                for analysis in analysis_results:
                    analysis_text += f"## {analysis['focus_area'].upper()} Analysis:\\n"
                    for finding in analysis['findings'][:3]:
                        analysis_text += f"- {finding}\\n"
                    
                    analysis_text += "\\nRecommendations:\\n"
                    for rec in analysis['recommendations'][:2]:
                        analysis_text += f"- Implement {rec.element_type} with {rec.psychology_principle}\\n"
                    
                    analysis_text += "\\n"
                
                return analysis_text
                
            except Exception as e:
                logger.error(f"Competition analysis failed: {e}")
                return f"Competitive analysis encountered an error: {e}"
        
        @self.agent.tool
        async def get_niche_insights(
            ctx: RunContext[AgentDependencies],
            niche: str,
            target_audience: str,
            conversion_goals: List[str]
        ) -> str:
            """Get niche-specific insights for conversion optimization.
            
            Args:
                niche: The business niche
                target_audience: Description of target audience
                conversion_goals: List of conversion goals (e.g., ["maximize_clicks", "build_trust"])
                
            Returns:
                Niche-specific conversion insights and recommendations
            """
            try:
                insights = []
                
                # Research for each conversion goal
                for goal in conversion_goals:
                    query = ResearchQuery(
                        topic=f"{goal} {niche} affiliate marketing {target_audience}",
                        focus_area="conversion",
                        niche_context=NicheType(niche.lower().replace(' ', '_')) if niche in ['fashion', 'tech', 'outdoor_gear'] else NicheType.GENERAL,
                        max_sources=3,
                        recency_days=365
                    )
                    
                    result = await self.web_research_tool.research(query)
                    insights.append({
                        'goal': goal,
                        'confidence': result.confidence_score,
                        'findings': result.findings[:2],
                        'recommendations': result.recommendations[:1]
                    })
                
                # Format insights
                insights_text = f"Niche Insights for {niche} - Target: {target_audience}:\\n\\n"
                
                for insight in insights:
                    insights_text += f"## {insight['goal'].replace('_', ' ').title()}:\\n"
                    insights_text += f"Confidence: {insight['confidence']:.2f}\\n\\n"
                    
                    for finding in insight['findings']:
                        insights_text += f"- {finding}\\n"
                    
                    if insight['recommendations']:
                        rec = insight['recommendations'][0]
                        insights_text += f"\\nRecommendation: Use {rec.element_type} with {rec.psychology_principle}\\n"
                        insights_text += f"Color Strategy: {rec.color_scheme}\\n"
                        insights_text += f"Placement: {rec.placement}\\n\\n"
                
                return insights_text
                
            except Exception as e:
                logger.error(f"Niche insights research failed: {e}")
                return f"Niche insights research encountered an error: {e}"
        
        @self.agent.tool
        async def research_performance_optimization(
            ctx: RunContext[AgentDependencies],
            website_type: str,
            current_performance: Dict[str, float],
            target_metrics: Dict[str, float]
        ) -> str:
            """Research performance optimization techniques for affiliate websites.
            
            Args:
                website_type: Type of website (e.g., "affiliate_marketing", "ecommerce")
                current_performance: Current performance metrics
                target_metrics: Target performance metrics
                
            Returns:
                Performance optimization recommendations
            """
            try:
                query = ResearchQuery(
                    topic=f"performance optimization {website_type} core web vitals",
                    focus_area="performance",
                    max_sources=4,
                    recency_days=180
                )
                
                result = await self.web_research_tool.research(query)
                
                # Create performance analysis
                perf_text = f"Performance Optimization Research for {website_type}:\\n\\n"
                perf_text += f"Research Confidence: {result.confidence_score:.2f}\\n\\n"
                
                perf_text += "Current vs Target Metrics:\\n"
                for metric, current_val in current_performance.items():
                    target_val = target_metrics.get(metric, current_val)
                    status = "✅ Good" if current_val >= target_val else "⚠️ Needs Improvement"
                    perf_text += f"- {metric}: {current_val} → {target_val} {status}\\n"
                
                perf_text += "\\nOptimization Findings:\\n"
                for finding in result.findings:
                    perf_text += f"- {finding}\\n"
                
                perf_text += "\\nImplementation Recommendations:\\n"
                for rec in result.recommendations:
                    perf_text += f"- {rec.psychology_principle}: {rec.text_content[:100]}...\\n"
                
                return perf_text
                
            except Exception as e:
                logger.error(f"Performance research failed: {e}")
                return f"Performance optimization research encountered an error: {e}"
    
    async def conduct_comprehensive_research(
        self,
        niche: str,
        target_audience: str,
        conversion_goals: List[str],
        deps: AgentDependencies
    ) -> ResearchResult:
        """Conduct comprehensive research for a specific use case."""
        try:
            # Create a comprehensive research prompt
            research_prompt = f"""
            Conduct comprehensive UI/UX and conversion optimization research for:
            
            Niche: {niche}
            Target Audience: {target_audience}
            Conversion Goals: {conversion_goals}
            
            Please research the following areas:
            1. Latest conversion optimization techniques for {niche} affiliate marketing
            2. Mobile-first design patterns that work best for {target_audience}
            3. Color psychology and trust signals for {niche} industry
            4. Performance optimization strategies for affiliate websites
            
            Focus on actionable insights that can be directly implemented to improve conversion rates.
            Provide specific recommendations with confidence scores.
            """
            
            # Run the agent
            result = await self.agent.run(
                research_prompt,
                deps=deps
            )
            
            return result.data
            
        except Exception as e:
            logger.error(f"Comprehensive research failed: {e}")
            raise
    
    async def quick_research(
        self,
        topic: str,
        niche: str = "general",
        focus_area: str = "conversion",
        deps: Optional[AgentDependencies] = None
    ) -> ResearchResult:
        """Conduct quick research on a specific topic."""
        if not deps:
            deps = AgentDependencies()
        
        try:
            research_prompt = f"""
            Research the topic: "{topic}" 
            
            Context:
            - Niche: {niche}
            - Focus Area: {focus_area}
            
            Please provide:
            1. Latest insights and best practices
            2. Specific implementation recommendations
            3. Conversion optimization elements
            4. Confidence assessment of findings
            
            Use the research tools to gather current information and provide actionable insights.
            """
            
            result = await self.agent.run(research_prompt, deps=deps)
            return result.data
            
        except Exception as e:
            logger.error(f"Quick research failed for '{topic}': {e}")
            raise