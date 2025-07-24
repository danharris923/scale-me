"""
Tests for all tools in the tools/ directory.

Comprehensive test suite covering web research, Google Sheets integration,
template generation, file generation, and SEO optimization tools.
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from pathlib import Path
from datetime import datetime, timedelta

# Web Research Tool
from tools.web_research import WebResearchTool, WebResearchError, RateLimiter, ResearchCache
from agents.models import ResearchQuery, ResearchResult, ConversionElement, NicheType

# Sheets Integration Tool
from tools.sheets_integration import SheetsIntegrationTool
from agents.models import GoogleSheetsConfig, ProductSchema

# Template Generator Tool
from tools.template_generator import TemplateGenerator

# File Generator Tool
from tools.file_generator import FileGenerator
from agents.models import WebsiteGenerationRequest, GeneratedWebsite

# SEO Optimizer Tool
from tools.seo_optimizer import SEOOptimizer
from agents.models import SEOOptimization

from config.settings import Settings


class TestWebResearchTool:
    """Tests for Web Research Tool."""
    
    @pytest.fixture
    def settings(self):
        return Settings()
    
    @pytest.fixture
    def research_tool(self, settings):
        return WebResearchTool(settings)
    
    @pytest.fixture
    def sample_query(self):
        return ResearchQuery(
            topic="conversion optimization for tech affiliate marketing",
            focus_area="conversion",
            niche_context=NicheType.TECH,
            max_sources=3,
            recency_days=365
        )
    
    def test_initialization(self, settings):
        """Test web research tool initialization."""
        tool = WebResearchTool(settings)
        
        assert tool.settings == settings
        assert tool.rate_limiter is not None
        assert tool.cache is not None
        assert isinstance(tool.blocked_domains, set)
        assert "ui_ux" in tool.research_sources
        assert "conversion" in tool.research_sources
    
    def test_get_relevant_sources(self, research_tool):
        """Test getting relevant sources for different focus areas."""
        # Test UI/UX sources
        sources = research_tool._get_relevant_sources("ui_ux")
        assert len(sources) > 0
        assert any("nngroup.com" in url for url in sources)
        
        # Test conversion sources
        sources = research_tool._get_relevant_sources("conversion")
        assert len(sources) > 0
        assert any("cxl.com" in url for url in sources)
        
        # Test with niche context
        sources = research_tool._get_relevant_sources("ui_ux", NicheType.TECH)
        assert len(sources) > 0
    
    def test_get_niche_sources(self, research_tool):
        """Test getting niche-specific sources."""
        # Test fashion niche
        sources = research_tool._get_niche_sources(NicheType.FASHION)
        assert len(sources) > 0
        assert any("vogue.com" in url for url in sources)
        
        # Test tech niche
        sources = research_tool._get_niche_sources(NicheType.TECH)
        assert len(sources) > 0
        assert any("techcrunch.com" in url for url in sources)
    
    @pytest.mark.asyncio
    async def test_check_robots_txt_allows(self, research_tool):
        """Test robots.txt checking when allowed."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = "User-agent: *\nAllow: /"
            
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = await research_tool._check_robots_txt("https://example.com/page")
            assert result is True
    
    @pytest.mark.asyncio
    async def test_check_robots_txt_error_handling(self, research_tool):
        """Test robots.txt error handling."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = Exception("Network error")
            
            result = await research_tool._check_robots_txt("https://example.com/page")
            assert result is True  # Should allow if can't check
    
    def test_extract_insights_conversion(self, research_tool):
        """Test insight extraction for conversion topics."""
        text = "The conversion rate increased when we used red buttons with urgency messaging."
        insights = research_tool._extract_insights(text, "conversion")
        
        assert len(insights) > 0
        assert any("conversion rate" in insight.lower() for insight in insights)
    
    def test_extract_insights_ui_ux(self, research_tool):
        """Test insight extraction for UI/UX topics."""
        text = "Mobile first design approach improved user experience significantly."
        insights = research_tool._extract_insights(text, "ui_ux")
        
        assert len(insights) > 0
        assert any("mobile first" in insight.lower() for insight in insights)
    
    def test_create_conversion_elements(self, research_tool):
        """Test conversion element creation from insights."""
        insights = [
            "Red buttons increase click-through rates for urgent actions",
            "Trust signals should be placed prominently in the header",
            "Social proof testimonials boost conversion rates"
        ]
        
        elements = research_tool._create_conversion_elements(insights, "conversion")
        
        assert len(elements) > 0
        for element in elements:
            assert isinstance(element, ConversionElement)
            assert element.element_type in ["button", "banner", "form", "card"]
            assert len(element.psychology_principle) > 0
            assert len(element.color_scheme) > 0
    
    def test_determine_element_type(self, research_tool):
        """Test element type determination from insights."""
        assert research_tool._determine_element_type("Click the red button") == "button"
        assert research_tool._determine_element_type("Header banner design") == "banner"
        assert research_tool._determine_element_type("Signup form optimization") == "form"
        assert research_tool._determine_element_type("Product showcase") == "card"
    
    def test_extract_psychology_principle(self, research_tool):
        """Test psychology principle extraction."""
        assert "urgency" in research_tool._extract_psychology_principle("Limited time offer")
        assert "trust" in research_tool._extract_psychology_principle("Secure payment processing")
        assert "social proof" in research_tool._extract_psychology_principle("Customer testimonials")
        assert "color psychology" in research_tool._extract_psychology_principle("Red color increases action")
    
    @pytest.mark.asyncio
    async def test_search_specific_topics(self, research_tool):
        """Test searching for specific topics."""
        with patch.object(research_tool, 'research') as mock_research:
            mock_result = ResearchResult(
                query="test topic",
                findings=["Finding 1", "Finding 2"],
                sources=["https://example.com"],
                recommendations=[],
                confidence_score=0.8,
                research_timestamp=datetime.now()
            )
            mock_research.return_value = mock_result
            
            topics = ["button design", "color psychology"]
            results = await research_tool.search_specific_topics(topics)
            
            assert len(results) == 2
            assert "button design" in results
            assert "color psychology" in results
            assert len(results["button design"]) == 2


class TestRateLimiter:
    """Tests for Rate Limiter."""
    
    @pytest.fixture
    def rate_limiter(self):
        return RateLimiter(requests_per_second=2.0)  # 2 requests per second
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self, rate_limiter):
        """Test that rate limiting works."""
        domain = "example.com"
        
        start_time = datetime.now()
        await rate_limiter.acquire(domain)
        await rate_limiter.acquire(domain)
        end_time = datetime.now()
        
        # Should take at least 0.5 seconds (1/2 requests per second)
        elapsed = (end_time - start_time).total_seconds()
        assert elapsed >= 0.4  # Some tolerance for timing


class TestResearchCache:
    """Tests for Research Cache."""
    
    @pytest.fixture
    def cache(self):
        return ResearchCache(ttl=1)  # 1 second TTL for testing
    
    def test_cache_operations(self, cache):
        """Test basic cache operations."""
        query = "test query"
        sources = ["https://example.com"]
        result = {"findings": ["test finding"]}
        
        # Test set and get
        cache.set(query, sources, result)
        cached_result = cache.get(query, sources)
        
        assert cached_result == result
    
    @pytest.mark.asyncio
    async def test_cache_expiration(self, cache):
        """Test cache expiration."""
        query = "test query"
        sources = ["https://example.com"]
        result = {"findings": ["test finding"]}
        
        cache.set(query, sources, result)
        await asyncio.sleep(1.1)  # Wait for TTL to expire
        
        cached_result = cache.get(query, sources)
        assert cached_result is None


class TestSheetsIntegrationTool:
    """Tests for Google Sheets Integration Tool."""
    
    @pytest.fixture
    def settings(self):
        return Settings()
    
    @pytest.fixture
    def sheets_tool(self, settings):
        return SheetsIntegrationTool(settings)
    
    @pytest.fixture
    def sample_config(self):
        return GoogleSheetsConfig(
            sheet_id="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
            range_name="Sheet1!A:G"
        )
    
    def test_initialization(self, settings):
        """Test sheets tool initialization."""
        tool = SheetsIntegrationTool(settings)
        assert tool.settings == settings
        assert tool.cache is not None
    
    @pytest.mark.asyncio
    async def test_test_connection_success(self, sheets_tool, sample_config):
        """Test successful connection test."""
        with patch.object(sheets_tool, 'get_products') as mock_get:
            mock_products = [
                ProductSchema(
                    id="1",
                    name="Test Product",
                    price=29.99,
                    image_url="https://example.com/image.jpg",
                    affiliate_url="https://example.com/affiliate",
                    category="electronics",
                    stock_status="in_stock"
                )
            ]
            mock_get.return_value = mock_products
            
            result = await sheets_tool.test_connection(sample_config)
            
            assert result['success'] is True
            assert 'headers' in result
            assert result['message'] == "Connection successful"
    
    @pytest.mark.asyncio
    async def test_test_connection_failure(self, sheets_tool, sample_config):
        """Test connection test failure."""
        with patch.object(sheets_tool, 'get_products') as mock_get:
            mock_get.side_effect = Exception("Invalid sheet ID")
            
            result = await sheets_tool.test_connection(sample_config)
            
            assert result['success'] is False
            assert "Invalid sheet ID" in result['message']


class TestTemplateGenerator:
    """Tests for Template Generator."""
    
    @pytest.fixture
    def template_generator(self):
        return TemplateGenerator("./templates")
    
    def test_initialization(self):
        """Test template generator initialization."""
        generator = TemplateGenerator("./templates")
        assert generator.template_dir == Path("./templates")
        assert generator.env is not None
    
    def test_generate_component_basic(self, template_generator):
        """Test basic component generation."""
        with patch.object(template_generator, '_load_template') as mock_load:
            mock_template = Mock()
            mock_template.render.return_value = "// Generated component"
            mock_load.return_value = mock_template
            
            result = template_generator.generate_component(
                component_name="TestComponent",
                template_name="TestComponent",
                props={"title": "string"},
                style="basic"
            )
            
            assert result == "// Generated component"
            mock_template.render.assert_called_once()
    
    def test_validate_typescript_valid(self, template_generator):
        """Test TypeScript validation with valid code."""
        valid_ts = """
        interface Props {
            title: string;
        }
        
        const Component: React.FC<Props> = ({ title }) => {
            return <div>{title}</div>;
        };
        
        export default Component;
        """
        
        result = template_generator.validate_typescript(valid_ts)
        assert result is True
    
    def test_validate_typescript_invalid(self, template_generator):
        """Test TypeScript validation with invalid code."""
        invalid_ts = "This is not valid TypeScript code !!!"
        
        result = template_generator.validate_typescript(invalid_ts)
        assert result is False


class TestFileGenerator:
    """Tests for File Generator."""
    
    @pytest.fixture
    def file_generator(self):
        return FileGenerator("./templates", "./test_generated")
    
    @pytest.fixture
    def sample_request(self):
        sheets_config = GoogleSheetsConfig(
            sheet_id="test_sheet_id",
            range_name="Sheet1!A:G"
        )
        
        return WebsiteGenerationRequest(
            niche=NicheType.TECH,
            brand_name="Test Brand",
            target_audience="Tech users",
            sheets_config=sheets_config,
            color_scheme="blue",
            features=["responsive_design"],
            conversion_goals=["maximize_clicks"]
        )
    
    def test_initialization(self):
        """Test file generator initialization."""
        generator = FileGenerator("./templates", "./output")
        assert generator.template_dir == Path("./templates")
        assert generator.output_dir == Path("./output")
        assert generator.template_generator is not None
    
    @pytest.mark.asyncio
    async def test_generate_website_structure(self, file_generator, sample_request):
        """Test website generation structure."""
        with patch.object(file_generator.template_generator, 'generate_page') as mock_page:
            with patch.object(file_generator.template_generator, 'generate_component') as mock_component:
                with patch.object(file_generator.template_generator, 'generate_api_route') as mock_api:
                    with patch.object(file_generator.template_generator, 'generate_config_file') as mock_config:
                        with patch.object(file_generator, '_write_file') as mock_write:
                            
                            mock_page.return_value = "// Page content"
                            mock_component.return_value = "// Component content"
                            mock_api.return_value = "// API content"
                            mock_config.return_value = "// Config content"
                            
                            result = await file_generator.generate_website(sample_request)
                            
                            assert isinstance(result, GeneratedWebsite)
                            assert result.project_name == "test-brand"
                            assert len(result.file_structure) > 0
                            assert "package.json" in result.file_structure
                            assert "vercel.json" in result.file_structure
    
    def test_get_env_vars(self, file_generator, sample_request):
        """Test environment variable generation."""
        env_vars = file_generator._get_env_vars(sample_request)
        
        assert "GOOGLE_SHEETS_API_KEY" in env_vars
        assert "NEXT_PUBLIC_BRAND_NAME" in env_vars
        assert env_vars["NEXT_PUBLIC_BRAND_NAME"] == "Test Brand"
        assert env_vars["NEXT_PUBLIC_NICHE"] == "tech"


class TestSEOOptimizer:
    """Tests for SEO Optimizer."""
    
    @pytest.fixture
    def seo_optimizer(self):
        return SEOOptimizer()
    
    def test_initialization(self):
        """Test SEO optimizer initialization."""
        optimizer = SEOOptimizer()
        assert optimizer.structured_data_schemas is not None
        assert len(optimizer.structured_data_schemas) > 0
    
    def test_generate_seo_optimization(self, seo_optimizer):
        """Test SEO optimization generation."""
        result = seo_optimizer.generate_seo_optimization(
            brand_name="Test Brand",
            niche=NicheType.TECH,
            target_keywords=["tech deals", "electronics"],
            description="Best tech deals online"
        )
        
        assert isinstance(result, SEOOptimization)
        assert len(result.meta_title) > 0
        assert len(result.meta_title) <= 60
        assert len(result.meta_description) > 0
        assert len(result.meta_description) <= 160
        assert len(result.keywords) > 0
        assert "website" in result.schema_markup
        assert "organization" in result.schema_markup
    
    def test_generate_meta_title_length_constraint(self, seo_optimizer):
        """Test meta title length constraints."""
        title = seo_optimizer._generate_meta_title(
            "Very Long Brand Name That Exceeds Normal Length",
            NicheType.TECH,
            ["very long keyword that might cause title to exceed limits"]
        )
        
        assert len(title) <= 60
    
    def test_expand_keywords(self, seo_optimizer):
        """Test keyword expansion."""
        keywords = seo_optimizer._expand_keywords(
            ["tech deals"],
            NicheType.TECH
        )
        
        assert len(keywords) <= 10
        assert "tech deals" in keywords
        assert "technology" in keywords
        assert "deals" in keywords
    
    def test_generate_product_schema(self, seo_optimizer):
        """Test product schema generation."""
        product = ProductSchema(
            id="test-product",
            name="Test Product",
            price=99.99,
            image_url="https://example.com/image.jpg",
            affiliate_url="https://example.com/buy",
            category="electronics",
            stock_status="in_stock"
        )
        
        schema = seo_optimizer.generate_product_schema(product, "https://example.com")
        
        assert schema["@type"] == "Product"
        assert schema["name"] == "Test Product"
        assert schema["offers"]["price"] == "99.99"
        assert schema["offers"]["availability"] == "https://schema.org/InStock"
    
    def test_generate_breadcrumb_schema(self, seo_optimizer):
        """Test breadcrumb schema generation."""
        breadcrumbs = [
            {"name": "Home", "url": "/"},
            {"name": "Tech", "url": "/tech"},
            {"name": "Laptops", "url": "/tech/laptops"}
        ]
        
        schema = seo_optimizer.generate_breadcrumb_schema(breadcrumbs, "https://example.com")
        
        assert schema["@type"] == "BreadcrumbList"
        assert len(schema["itemListElement"]) == 3
        assert schema["itemListElement"][0]["name"] == "Home"
    
    def test_generate_faq_schema(self, seo_optimizer):
        """Test FAQ schema generation."""
        faqs = [
            {"question": "What is the return policy?", "answer": "30 day returns"},
            {"question": "Do you offer warranties?", "answer": "Yes, 1 year warranty"}
        ]
        
        schema = seo_optimizer.generate_faq_schema(faqs)
        
        assert schema["@type"] == "FAQPage"
        assert len(schema["mainEntity"]) == 2
        assert schema["mainEntity"][0]["name"] == "What is the return policy?"
    
    def test_generate_robots_txt(self, seo_optimizer):
        """Test robots.txt generation."""
        robots_txt = seo_optimizer.generate_robots_txt("https://example.com")
        
        assert "User-agent: *" in robots_txt
        assert "Allow: /" in robots_txt
        assert "Disallow: /api/" in robots_txt
        assert "Sitemap: https://example.com/sitemap.xml" in robots_txt
    
    def test_optimize_images_metadata(self, seo_optimizer):
        """Test image metadata optimization."""
        images = [
            {"src": "/images/product-image.jpg"},
            {"src": "/images/hero-banner.png", "alt": "Existing alt text"}
        ]
        
        optimized = seo_optimizer.optimize_images_metadata(images)
        
        assert len(optimized) == 2
        assert optimized[0]["alt"] == "Product Image"  # Generated from filename
        assert optimized[1]["alt"] == "Existing alt text"  # Preserved existing
        assert all(img.get("loading") == "lazy" for img in optimized)
        assert all(img.get("width") and img.get("height") for img in optimized)
    
    def test_generate_meta_tags(self, seo_optimizer):
        """Test meta tags generation."""
        seo_data = SEOOptimization(
            meta_title="Test Title",
            meta_description="Test Description",
            keywords=["test", "keywords"],
            schema_markup={},
            performance_targets={}
        )
        
        page_data = {
            "url": "https://example.com/page",
            "image": "https://example.com/image.jpg",
            "site_name": "Test Site"
        }
        
        meta_tags = seo_optimizer.generate_meta_tags(seo_data, page_data)
        
        assert meta_tags["title"] == "Test Title"
        assert meta_tags["description"] == "Test Description"
        assert meta_tags["og:title"] == "Test Title"
        assert meta_tags["twitter:card"] == "summary_large_image"
        assert "robots" in meta_tags