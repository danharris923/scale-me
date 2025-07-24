"""
Web research tool for gathering UI/UX and conversion optimization insights.

This module provides ethical web scraping capabilities for researching:
- UI/UX conversion best practices
- Latest Tailwind CSS patterns and components
- SEO optimization techniques
- Accessibility standards

Respects robots.txt and implements rate limiting to avoid overwhelming servers.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import json
import hashlib

import httpx
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from agents.models import ResearchQuery, ResearchResult, ConversionElement, NicheType
from config import Settings

logger = logging.getLogger(__name__)


class WebResearchError(Exception):
    """Custom exception for web research errors."""
    pass


class RateLimiter:
    """Simple rate limiter to avoid overwhelming servers."""
    
    def __init__(self, requests_per_second: float = 1.0):
        self.requests_per_second = requests_per_second
        self.last_request_time = {}
        self.min_interval = 1.0 / requests_per_second
    
    async def acquire(self, domain: str) -> None:
        """Wait if necessary to respect rate limits."""
        current_time = datetime.now()
        
        if domain in self.last_request_time:
            time_since_last = (current_time - self.last_request_time[domain]).total_seconds()
            if time_since_last < self.min_interval:
                sleep_time = self.min_interval - time_since_last
                await asyncio.sleep(sleep_time)
        
        self.last_request_time[domain] = datetime.now()


class ResearchCache:
    """Cache for storing research results."""
    
    def __init__(self, ttl: int = 3600):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl
    
    def _generate_key(self, query: str, sources: List[str]) -> str:
        """Generate cache key from query and sources."""
        content = f"{query}-{'-'.join(sorted(sources))}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, query: str, sources: List[str]) -> Optional[Dict[str, Any]]:
        """Get cached research results."""
        key = self._generate_key(query, sources)
        if key not in self._cache:
            return None
        
        data = self._cache[key]
        if datetime.now() > data['expires_at']:
            del self._cache[key]
            return None
        
        return data['result']
    
    def set(self, query: str, sources: List[str], result: Dict[str, Any]) -> None:
        """Cache research results."""
        key = self._generate_key(query, sources)
        self._cache[key] = {
            'result': result,
            'expires_at': datetime.now() + timedelta(seconds=self.ttl)
        }


class WebResearchTool:
    """Tool for researching UI/UX and conversion optimization techniques."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.rate_limiter = RateLimiter(requests_per_second=0.5)  # Conservative rate limiting
        self.cache = ResearchCache(ttl=3600)  # 1 hour cache
        self.blocked_domains: Set[str] = set()
        
        # Research sources for different topics
        self.research_sources = {
            'ui_ux': [
                'https://www.nngroup.com',
                'https://uxplanet.org',
                'https://www.smashingmagazine.com',
                'https://medium.com/topic/design',
                'https://www.interaction-design.org'
            ],
            'conversion': [
                'https://cxl.com',
                'https://www.optimizely.com/insights',
                'https://blog.hubspot.com/marketing/conversion-optimization',
                'https://unbounce.com/conversion-rate-optimization',
                'https://www.crazyegg.com/blog'
            ],
            'tailwind': [
                'https://tailwindcss.com/docs',
                'https://tailwindui.com/components',
                'https://headlessui.com',
                'https://heroicons.com',
                'https://github.com/tailwindlabs'
            ],
            'seo': [
                'https://developers.google.com/search',
                'https://moz.com/blog',
                'https://searchengineland.com',
                'https://backlinko.com',
                'https://www.semrush.com/blog'
            ]
        }
    
    async def research(
        self, 
        query: ResearchQuery, 
        max_sources: Optional[int] = None
    ) -> ResearchResult:
        """Conduct research on a specific topic."""
        max_sources = max_sources or query.max_sources
        
        # Check cache first
        sources = self._get_relevant_sources(query.focus_area, query.niche_context)
        cached_result = self.cache.get(query.topic, sources[:max_sources])
        if cached_result:
            logger.info(f"Returning cached research for: {query.topic}")
            return ResearchResult(**cached_result)
        
        try:
            # Perform research
            research_results = await self._perform_research(query, max_sources)
            
            # Analyze and synthesize findings
            result = await self._synthesize_findings(query, research_results)
            
            # Cache results
            self.cache.set(query.topic, sources[:max_sources], result.dict())
            
            return result
            
        except Exception as e:
            logger.error(f"Research failed for '{query.topic}': {e}")
            raise WebResearchError(f"Research failed: {e}")
    
    def _get_relevant_sources(
        self, 
        focus_area: str, 
        niche_context: Optional[NicheType] = None
    ) -> List[str]:
        """Get relevant research sources for the focus area."""
        base_sources = self.research_sources.get(focus_area, [])
        
        # Add niche-specific sources if available
        if niche_context:
            niche_sources = self._get_niche_sources(niche_context)
            base_sources.extend(niche_sources)
        
        # Filter out blocked domains
        return [url for url in base_sources if urlparse(url).netloc not in self.blocked_domains]
    
    def _get_niche_sources(self, niche: NicheType) -> List[str]:
        """Get niche-specific research sources."""
        niche_sources = {
            NicheType.FASHION: [
                'https://www.vogue.com/fashion',
                'https://fashionista.com',
                'https://www.refinery29.com/en-us/fashion'
            ],
            NicheType.TECH: [
                'https://techcrunch.com',
                'https://www.theverge.com',
                'https://arstechnica.com'
            ],
            NicheType.OUTDOOR_GEAR: [
                'https://www.outsideonline.com',
                'https://www.rei.com/blog',
                'https://www.backpacker.com'
            ]
        }
        return niche_sources.get(niche, [])
    
    async def _perform_research(
        self, 
        query: ResearchQuery, 
        max_sources: int
    ) -> List[Dict[str, Any]]:
        """Perform actual web research."""
        sources = self._get_relevant_sources(query.focus_area, query.niche_context)[:max_sources]
        research_results = []
        
        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(3)  # Max 3 concurrent requests
        
        async def research_source(source_url: str) -> Optional[Dict[str, Any]]:
            async with semaphore:
                try:
                    # Check robots.txt first
                    if not await self._check_robots_txt(source_url):
                        logger.warning(f"Robots.txt disallows scraping {source_url}")
                        return None
                    
                    # Rate limiting
                    domain = urlparse(source_url).netloc
                    await self.rate_limiter.acquire(domain)
                    
                    # Scrape content
                    content = await self._scrape_content(source_url, query.topic)
                    if content:
                        return {
                            'url': source_url,
                            'title': content.get('title', ''),
                            'content': content.get('text', ''),
                            'insights': content.get('insights', [])
                        }
                    
                except Exception as e:
                    logger.warning(f"Failed to research {source_url}: {e}")
                    # Add to blocked domains if consistently failing
                    domain = urlparse(source_url).netloc
                    self.blocked_domains.add(domain)
                
                return None
        
        # Research all sources concurrently
        tasks = [research_source(url) for url in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter successful results
        research_results = [r for r in results if isinstance(r, dict) and r is not None]
        
        return research_results
    
    async def _check_robots_txt(self, url: str) -> bool:
        """Check if robots.txt allows scraping."""
        try:
            parsed_url = urlparse(url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(robots_url)
                
                if response.status_code == 200:
                    rp = RobotFileParser()
                    rp.set_url(robots_url)
                    rp.read()
                    return rp.can_fetch('*', url)
                
        except Exception as e:
            logger.debug(f"Could not check robots.txt for {url}: {e}")
        
        # Allow if we can't check robots.txt
        return True
    
    async def _scrape_content(self, url: str, topic: str) -> Optional[Dict[str, Any]]:
        """Scrape content from a URL."""
        try:
            async with httpx.AsyncClient(
                timeout=30.0,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            ) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract relevant content
                content = self._extract_relevant_content(soup, topic)
                
                return {
                    'title': soup.title.string if soup.title else '',
                    'text': content['text'],
                    'insights': content['insights']
                }
                
        except Exception as e:
            logger.warning(f"Failed to scrape {url}: {e}")
            return None
    
    def _extract_relevant_content(self, soup: BeautifulSoup, topic: str) -> Dict[str, Any]:
        """Extract content relevant to the research topic."""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Extract insights based on keywords
        insights = self._extract_insights(text, topic)
        
        return {
            'text': text[:5000],  # Limit text length
            'insights': insights
        }
    
    def _extract_insights(self, text: str, topic: str) -> List[str]:
        """Extract relevant insights from text content."""
        insights = []
        text_lower = text.lower()
        
        # Define insight patterns for different topics
        insight_patterns = {
            'conversion': [
                'conversion rate', 'cta', 'call to action', 'button design',
                'trust signal', 'social proof', 'urgency', 'scarcity',
                'color psychology', 'psychology', 'persuasion'
            ],
            'ui_ux': [
                'user experience', 'usability', 'accessibility', 'mobile first',
                'responsive design', 'user interface', 'design pattern',
                'navigation', 'layout'
            ],
            'seo': [
                'search engine optimization', 'meta tags', 'structured data',
                'page speed', 'core web vitals', 'lighthouse', 'performance'
            ],
            'tailwind': [
                'tailwind', 'utility classes', 'component', 'responsive',
                'dark mode', 'customize'
            ]
        }
        
        # Find sentences containing relevant keywords
        sentences = text.split('.')
        for sentence in sentences[:50]:  # Limit to first 50 sentences
            sentence_lower = sentence.lower().strip()
            if len(sentence_lower) < 20:  # Skip very short sentences
                continue
                
            for pattern in insight_patterns.get(topic, []):
                if pattern in sentence_lower:
                    insights.append(sentence.strip())
                    break
        
        return insights[:10]  # Return top 10 insights
    
    async def _synthesize_findings(
        self, 
        query: ResearchQuery, 
        research_results: List[Dict[str, Any]]
    ) -> ResearchResult:
        """Synthesize research findings into structured result."""
        all_findings = []
        all_insights = []
        sources = []
        
        for result in research_results:
            if result['insights']:
                all_insights.extend(result['insights'])
            
            sources.append(result['url'])
            
            # Add general findings
            if result['content']:
                all_findings.append(f"From {urlparse(result['url']).netloc}: {result['content'][:200]}...")
        
        # Create conversion elements from insights
        recommendations = self._create_conversion_elements(all_insights, query.focus_area)
        
        # Calculate confidence score based on number of sources and quality
        confidence_score = min(1.0, len(research_results) / query.max_sources * 0.8 + 0.2)
        
        return ResearchResult(
            query=query.topic,
            findings=all_findings[:10],  # Top 10 findings
            sources=sources,
            recommendations=recommendations,
            confidence_score=confidence_score,
            research_timestamp=datetime.now()
        )
    
    def _create_conversion_elements(
        self, 
        insights: List[str], 
        focus_area: str
    ) -> List[ConversionElement]:
        """Create conversion elements from research insights."""
        elements = []
        
        # Analyze insights and create conversion elements
        for insight in insights[:5]:  # Top 5 insights
            element_type = self._determine_element_type(insight)
            psychology_principle = self._extract_psychology_principle(insight)
            color_scheme = self._suggest_color_scheme(insight, focus_area)
            
            element = ConversionElement(
                element_type=element_type,
                psychology_principle=psychology_principle,
                color_scheme=color_scheme,
                text_content=insight[:100] + '...' if len(insight) > 100 else insight,
                placement=self._suggest_placement(element_type)
            )
            
            elements.append(element)
        
        return elements
    
    def _determine_element_type(self, insight: str) -> str:
        """Determine UI element type from insight."""
        insight_lower = insight.lower()
        
        if any(word in insight_lower for word in ['button', 'cta', 'click']):
            return 'button'
        elif any(word in insight_lower for word in ['banner', 'header', 'hero']):
            return 'banner'
        elif any(word in insight_lower for word in ['form', 'input', 'signup']):
            return 'form'
        else:
            return 'card'
    
    def _extract_psychology_principle(self, insight: str) -> str:
        """Extract psychology principle from insight."""
        insight_lower = insight.lower()
        
        if any(word in insight_lower for word in ['urgency', 'limited', 'hurry']):
            return 'urgency/scarcity'
        elif any(word in insight_lower for word in ['trust', 'secure', 'safe']):
            return 'trust building'
        elif any(word in insight_lower for word in ['social', 'proof', 'testimonial']):
            return 'social proof'
        elif any(word in insight_lower for word in ['color', 'red', 'green', 'blue']):
            return 'color psychology'
        else:
            return 'general persuasion'
    
    def _suggest_color_scheme(self, insight: str, focus_area: str) -> str:
        """Suggest color scheme based on insight and focus area."""
        insight_lower = insight.lower()
        
        if 'red' in insight_lower or 'urgency' in insight_lower:
            return 'red for urgency and action'
        elif 'green' in insight_lower or 'trust' in insight_lower:
            return 'green for trust and success'
        elif 'blue' in insight_lower or focus_area == 'ui_ux':
            return 'blue for professionalism and trust'
        else:
            return 'brand-consistent colors'
    
    def _suggest_placement(self, element_type: str) -> str:
        """Suggest optimal placement for element type."""
        placements = {
            'button': 'above the fold, right-aligned',
            'banner': 'top of page or sticky header',
            'form': 'center of page or sidebar',
            'card': 'grid layout with proper spacing'
        }
        return placements.get(element_type, 'prominently visible')
    
    async def search_specific_topics(
        self, 
        topics: List[str], 
        focus_area: str = 'conversion'
    ) -> Dict[str, List[str]]:
        """Search for specific topics and return findings."""
        results = {}
        
        for topic in topics:
            query = ResearchQuery(
                topic=topic,
                focus_area=focus_area,
                max_sources=3,
                recency_days=365
            )
            
            try:
                result = await self.research(query)
                results[topic] = result.findings
            except Exception as e:
                logger.warning(f"Failed to research topic '{topic}': {e}")
                results[topic] = []
        
        return results