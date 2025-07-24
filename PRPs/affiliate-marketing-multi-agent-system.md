name: "Multi-Agent Affiliate Marketing Website Generator"
description: |

## Purpose
Build a sophisticated Pydantic AI multi-agent system that generates production-ready, SEO-optimized affiliate marketing websites using React + Vercel stack with Google Sheets integration. The system uses a Website Generator Agent with a Research Agent as a tool to create high-converting, modern affiliate sites.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Be sure to follow all rules in CLAUDE.md

---

## Goal
Create a production-ready multi-agent system where users can generate complete affiliate marketing websites through a CLI interface. The Website Generator Agent uses a Research Agent as a tool to incorporate real-time UI/UX research, conversion optimization techniques, and latest web development best practices into generated React + Vercel templates.

## Why
- **Business value**: Automates creation of high-converting affiliate marketing websites
- **Integration**: Demonstrates advanced Pydantic AI multi-agent patterns with real-world application
- **Problems solved**: Eliminates manual website setup, incorporates latest conversion psychology, provides SEO-optimized templates
- **Target users**: Affiliate marketers, agencies, developers needing fast deployment

## What
A CLI-based application where:
- Users specify affiliate niche and requirements
- Website Generator Agent creates complete React/Next.js template
- Research Agent provides real-time UI/UX and conversion optimization research
- Generated websites include Google Sheets integration for product data
- Output is deployment-ready for Vercel with automated builds
- Templates support multiple niches (outdoor gear, fashion, tech, etc.)

### Success Criteria
- [ ] Website Generator Agent creates production-ready React/Next.js templates
- [ ] Research Agent provides accurate UI/UX conversion optimization research
- [ ] Generated websites achieve 90+ Lighthouse scores
- [ ] Google Sheets integration works with real-time product updates
- [ ] Vercel deployment pipeline is fully automated
- [ ] Templates follow mobile-first, conversion-optimized design principles
- [ ] All tests pass and code meets quality standards
- [ ] Generated sites load in under 2 seconds

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window

# Pydantic AI Multi-Agent System
- file: D:\git\scale-me\site\research\pydantic-ai\homepage.md
  why: Core framework overview and capabilities
  
- file: D:\git\scale-me\site\research\pydantic-ai\agents.md
  why: Agent creation patterns, system prompts, tools, dependencies
  
- file: D:\git\scale-me\site\research\pydantic-ai\multi-agent.md
  why: Multi-agent system patterns, agent delegation, agent-as-tool patterns
  
- file: D:\git\scale-me\site\research\pydantic-ai\tools.md
  why: Tool creation, context-aware tools, retry mechanisms, validation
  
- file: D:\git\scale-me\site\research\pydantic-ai\models.md
  why: Model provider configuration, fallback models, API key setup

# React + Next.js Frontend
- file: D:\git\scale-me\site\research\react\homepage.md
  why: Core React concepts, component patterns, performance optimization
  
- file: D:\git\scale-me\site\research\react\describing-ui.md
  why: Component creation, JSX syntax, props, conditional rendering
  
- file: D:\git\scale-me\site\research\react\adding-interactivity.md
  why: Event handling, state management, hooks patterns
  
- file: D:\git\scale-me\site\research\nextjs\overview.md
  why: Next.js framework features, App Router, Server/Client components
  
- file: D:\git\scale-me\site\research\nextjs\routing.md
  why: File-based routing, dynamic routes, layouts, route handlers
  
- file: D:\git\scale-me\site\research\nextjs\data-fetching.md
  why: Server components, caching strategies, streaming patterns

# Styling and UI
- file: D:\git\scale-me\site\research\tailwind\overview.md
  why: Utility-first approach, responsive design, customization
  
- file: D:\git\scale-me\site\research\tailwind\utility-first.md
  why: Core philosophy, state variants, dark mode, responsive patterns
  
- file: D:\git\scale-me\site\research\tailwind\ecommerce-components.md
  why: 80+ pre-built e-commerce components from Tailwind Plus

# Deployment and Backend
- file: D:\git\scale-me\site\research\vercel\overview.md
  why: Platform capabilities, deployment strategies, optimization
  
- file: D:\git\scale-me\site\research\vercel\getting-started.md
  why: CLI installation, deployment approaches, project setup
  
- file: D:\git\scale-me\site\research\vercel\environment-variables.md
  why: Configuration management, API key storage, build variables

# Data Integration
- file: D:\git\scale-me\site\research\google-cloud\sheets-api.md
  why: Google Sheets API integration, authentication, real-time data access

# Code Examples and Patterns
- file: D:\git\scale-me\site\PRPs\EXAMPLE_multi_agent_prp.md
  why: Multi-agent system implementation patterns and structure
  
- url: https://ai.pydantic.dev/examples/
  why: Official Pydantic AI examples for reference patterns
  
- url: https://vercel.com/templates/next.js
  why: Next.js template examples for inspiration and patterns
  
- url: https://tailwindui.com/components
  why: Production-ready component examples
```

### Current Codebase tree
```bash
D:\git\scale-me\site\
├── CLAUDE.md                   # Project guidelines and instructions
├── initial.md                  # Feature requirements and tech stack
├── PRPs/
│   ├── EXAMPLE_multi_agent_prp.md
│   └── templates/
│       └── prp_base.md
├── research/                   # Comprehensive documentation research
│   ├── pydantic-ai/
│   │   ├── homepage.md
│   │   ├── agents.md
│   │   ├── multi-agent.md
│   │   ├── tools.md
│   │   └── models.md
│   ├── react/
│   │   ├── homepage.md
│   │   ├── describing-ui.md
│   │   └── adding-interactivity.md
│   ├── nextjs/
│   │   ├── overview.md
│   │   ├── routing.md
│   │   └── data-fetching.md
│   ├── tailwind/
│   │   ├── overview.md
│   │   ├── utility-first.md
│   │   └── ecommerce-components.md
│   ├── vercel/
│   │   ├── overview.md
│   │   ├── getting-started.md
│   │   └── environment-variables.md
│   └── google-cloud/
│       └── sheets-api.md
└── README.md
```

### Desired Codebase tree with files to be added
```bash
D:\git\scale-me\site\
├── agents/
│   ├── __init__.py                    # Package init
│   ├── website_generator_agent.py     # Primary agent - creates complete websites
│   ├── research_agent.py              # Sub-agent - provides UI/UX research
│   ├── providers.py                   # LLM provider configuration
│   └── models.py                      # Pydantic models for data validation
├── tools/
│   ├── __init__.py                    # Package init
│   ├── file_generator.py              # React/Next.js file generation
│   ├── web_research.py                # Web scraping for real-time research
│   ├── sheets_integration.py          # Google Sheets API integration
│   ├── template_generator.py          # Website template scaffolding
│   └── seo_optimizer.py               # SEO optimization tools
├── templates/
│   ├── __init__.py                    # Package init
│   ├── react/
│   │   ├── components/                # React component templates
│   │   │   ├── ProductCard.tsx.template
│   │   │   ├── Hero.tsx.template
│   │   │   ├── Navigation.tsx.template
│   │   │   └── Footer.tsx.template
│   │   └── hooks/                     # Custom hook templates
│   │       └── useGoogleSheets.ts.template
│   ├── nextjs/
│   │   ├── pages/                     # Next.js page templates
│   │   │   ├── index.tsx.template
│   │   │   ├── category/[slug].tsx.template
│   │   │   └── product/[id].tsx.template
│   │   ├── layouts/                   # Layout templates
│   │   │   └── DefaultLayout.tsx.template
│   │   └── api/                       # API route templates
│   │       └── sheets.ts.template
│   ├── tailwind/
│   │   ├── components/                # Tailwind component patterns
│   │   │   ├── ecommerce.css
│   │   │   └── conversion-optimized.css
│   │   └── config/
│   │       └── tailwind.config.js.template
│   └── vercel/
│       ├── vercel.json.template       # Vercel configuration
│       └── .env.example.template      # Environment variables template
├── config/
│   ├── __init__.py                    # Package init
│   └── settings.py                    # Environment and config management
├── tests/
│   ├── __init__.py                    # Package init
│   ├── test_website_generator.py      # Website generator tests
│   ├── test_research_agent.py         # Research agent tests
│   ├── test_file_generator.py         # File generation tests
│   ├── test_web_research.py           # Web research tests
│   ├── test_sheets_integration.py     # Google Sheets tests
│   ├── test_template_generator.py     # Template generation tests
│   └── test_cli.py                    # CLI tests
├── cli.py                             # CLI interface with streaming
├── .env.example                       # Environment variables template
├── requirements.txt                   # Updated dependencies
├── Dockerfile                         # Docker development environment
├── docker-compose.yml                 # Development services
├── README.md                          # Comprehensive documentation
└── generated/                         # Output directory for generated websites
    └── .gitkeep                       # Keep directory in git
```

### Known Gotchas & Library Quirks
```python
# CRITICAL: Pydantic AI requires async throughout - no sync functions in async context
# CRITICAL: React templates must use TypeScript for type safety
# CRITICAL: Next.js App Router uses different patterns than Pages Router
# CRITICAL: Tailwind CSS classes must be purged correctly for production
# CRITICAL: Google Sheets API requires OAuth2 or Service Account authentication
# CRITICAL: Vercel environment variables need different handling for build vs runtime
# CRITICAL: Agent-as-tool pattern requires passing ctx.usage for token tracking
# CRITICAL: File generation must handle Windows/Unix path differences
# CRITICAL: Template placeholders must use consistent variable naming
# CRITICAL: Always validate generated HTML/CSS for accessibility standards
# CRITICAL: Mobile-first responsive design is mandatory for conversion
# CRITICAL: SEO meta tags must be dynamically generated based on content
# CRITICAL: Performance budgets: React bundle <100KB, images <500KB, TTI <3s
```

## Implementation Blueprint

### Data models and structure

```python
# models.py - Core data structures for the multi-agent system
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum

class NicheType(str, Enum):
    OUTDOOR_GEAR = "outdoor_gear"
    FASHION = "fashion"
    TECH = "tech"
    HOME_IMPROVEMENT = "home_improvement"
    MUSIC = "music"
    GENERAL = "general"

class ConversionElement(BaseModel):
    """UI element optimized for conversion"""
    element_type: Literal["button", "card", "banner", "form"]
    psychology_principle: str = Field(..., description="Psychology principle applied")
    color_scheme: str = Field(..., description="Color psychology rationale")
    text_content: str = Field(..., description="Conversion-optimized copy")
    placement: str = Field(..., description="Optimal placement strategy")

class SEOOptimization(BaseModel):
    """SEO optimization recommendations"""
    meta_title: str = Field(..., max_length=60)
    meta_description: str = Field(..., max_length=160)
    keywords: List[str] = Field(..., min_items=3, max_items=10)
    schema_markup: Dict[str, Any] = Field(default_factory=dict)
    performance_targets: Dict[str, float] = Field(default_factory=lambda: {
        "lighthouse_score": 90.0,
        "ttfb": 800.0,  # milliseconds
        "lcp": 2500.0,  # milliseconds
        "cls": 0.1
    })

class GoogleSheetsConfig(BaseModel):
    """Google Sheets integration configuration"""
    sheet_id: str = Field(..., description="Google Sheets ID")
    range_name: str = Field(default="Sheet1!A:Z")
    api_key: Optional[str] = Field(None, description="API key for public sheets")
    service_account_path: Optional[str] = Field(None, description="Service account JSON path")
    cache_duration: int = Field(default=300, description="Cache duration in seconds")

class ProductSchema(BaseModel):
    """Product data structure from Google Sheets"""
    id: str
    name: str
    price: float
    image_url: HttpUrl
    affiliate_url: HttpUrl
    category: str
    description: Optional[str] = None
    discount_percent: Optional[float] = Field(None, ge=0, le=100)
    is_featured: bool = False
    stock_status: Literal["in_stock", "low_stock", "out_of_stock"] = "in_stock"

class WebsiteGenerationRequest(BaseModel):
    """Request to generate affiliate marketing website"""
    niche: NicheType
    brand_name: str = Field(..., min_length=2, max_length=50)
    domain_name: Optional[str] = None
    color_scheme: str = Field(default="blue", description="Primary color theme")
    target_audience: str = Field(..., description="Target customer description")
    sheets_config: GoogleSheetsConfig
    features: List[str] = Field(default_factory=lambda: [
        "product_catalog", "category_pages", "search", "mobile_responsive", "seo_optimized"
    ])
    conversion_goals: List[str] = Field(default_factory=lambda: [
        "maximize_clicks", "build_trust", "reduce_bounce_rate"
    ])

class GeneratedWebsite(BaseModel):
    """Complete generated website structure"""
    project_name: str
    file_structure: Dict[str, str] = Field(..., description="File path to content mapping")
    package_json: Dict[str, Any]
    vercel_config: Dict[str, Any]
    environment_variables: Dict[str, str]
    deployment_url: Optional[HttpUrl] = None
    performance_metrics: Optional[Dict[str, float]] = None
    generation_timestamp: datetime = Field(default_factory=datetime.now)

class ResearchQuery(BaseModel):
    """Research query for the Research Agent"""
    topic: str = Field(..., description="Research topic")
    focus_area: Literal["ui_ux", "conversion", "seo", "performance", "accessibility"]
    niche_context: Optional[NicheType] = None
    max_sources: int = Field(default=5, ge=1, le=20)
    recency_days: int = Field(default=365, description="How recent should sources be")

class ResearchResult(BaseModel):
    """Research findings from Research Agent"""
    query: str
    findings: List[str] = Field(..., min_items=1)
    sources: List[HttpUrl] = Field(default_factory=list)
    recommendations: List[ConversionElement] = Field(default_factory=list)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    research_timestamp: datetime = Field(default_factory=datetime.now)

class AgentDependencies(BaseModel):
    """Dependencies injected into agents"""
    api_keys: Dict[str, str] = Field(default_factory=dict)
    output_directory: str = Field(default="./generated")
    template_directory: str = Field(default="./templates")
    research_cache: Dict[str, Any] = Field(default_factory=dict)
    performance_targets: SEOOptimization = Field(default_factory=SEOOptimization)
```

### List of tasks to be completed

```yaml
Task 1: Setup Configuration and Environment
CREATE config/settings.py:
  - PATTERN: Use pydantic-settings for environment management
  - Load API keys for LLM providers, Google Sheets, web scraping
  - Validate required configurations on startup
  - Support multiple LLM providers with fallbacks

CREATE .env.example:
  - Include all required environment variables with descriptions
  - LLM provider configurations (OpenAI, Anthropic, etc.)
  - Google Sheets API credentials
  - Web scraping service keys

Task 2: Implement Core Template System
CREATE templates/ directory structure:
  - PATTERN: Jinja2-style templates with variable substitution
  - React component templates with TypeScript
  - Next.js page templates with App Router patterns
  - Tailwind CSS utility patterns for conversion optimization
  - Vercel deployment configurations

CREATE tools/template_generator.py:
  - PATTERN: Template rendering with context injection
  - File generation with proper directory structure
  - Variable substitution for branding and configuration
  - Validation of generated code syntax

Task 3: Implement Google Sheets Integration
CREATE tools/sheets_integration.py:
  - PATTERN: OAuth2 flow for user sheets or Service Account for automation
  - Real-time data fetching with caching
  - Data validation against ProductSchema
  - Error handling for API rate limits and authentication

Task 4: Implement Web Research Tool
CREATE tools/web_research.py:
  - PATTERN: Web scraping with respect for robots.txt
  - Research UI/UX conversion best practices
  - Latest Tailwind CSS patterns and components
  - SEO optimization techniques
  - Cache research results to avoid duplicate requests

Task 5: Create Research Agent
CREATE agents/research_agent.py:
  - PATTERN: Follow Pydantic AI agent creation patterns
  - Use web_research tool for gathering information
  - System prompt focused on UI/UX and conversion research
  - Return structured ResearchResult objects
  - Cache findings to optimize performance

Task 6: Implement File Generation Tools
CREATE tools/file_generator.py:
  - PATTERN: File system operations with proper error handling
  - Generate React components with TypeScript
  - Create Next.js pages with proper routing
  - Generate package.json with correct dependencies
  - Create Vercel configuration files

CREATE tools/seo_optimizer.py:
  - PATTERN: SEO best practices implementation
  - Generate meta tags and structured data
  - Optimize images and performance
  - Create sitemap and robots.txt
  - Implement accessibility standards

Task 7: Create Website Generator Agent
CREATE agents/website_generator_agent.py:
  - PATTERN: Primary agent with research agent as tool
  - Orchestrate entire website generation process
  - Use research findings to inform design decisions
  - Generate complete project structure
  - Validate generated code and configuration

Task 8: Implement CLI Interface
CREATE cli.py:
  - PATTERN: Rich CLI with streaming output and progress bars
  - Interactive prompts for website configuration
  - Real-time display of agent work and tool usage
  - Error handling and user guidance
  - Option to review generated code before deployment

Task 9: Add Comprehensive Testing
CREATE tests/ directory:
  - PATTERN: pytest with async support and mocking
  - Unit tests for all tools and agents
  - Integration tests for complete website generation
  - Performance tests for generated websites
  - Validation tests for Lighthouse scores

Task 10: Create Documentation and Examples
CREATE README.md:
  - PATTERN: Comprehensive setup and usage guide
  - Architecture explanation with diagrams
  - Configuration examples and troubleshooting
  - Sample generated websites showcase
  - Performance benchmarks and optimization tips

CREATE Docker development environment:
  - PATTERN: Multi-stage Dockerfile for development and testing
  - docker-compose.yml with required services
  - Volume mounting for live development
  - Environment variable management
```

### Per task pseudocode

```python
# Task 5: Research Agent Implementation
class ResearchAgent:
    """Agent specialized in UI/UX and conversion research"""
    
    def __init__(self, model: str, deps: AgentDependencies):
        self.agent = Agent(
            model=model,
            deps_type=AgentDependencies,
            output_type=ResearchResult,
            system_prompt="""You are a UI/UX and conversion optimization research specialist.
            Your role is to research the latest trends, best practices, and proven techniques
            for creating high-converting affiliate marketing websites.
            
            Focus areas:
            - Conversion psychology and user behavior
            - Mobile-first responsive design patterns
            - Color psychology and trust signals
            - Latest Tailwind CSS component patterns
            - Performance optimization techniques
            - Accessibility standards
            
            Always provide specific, actionable recommendations with confidence scores."""
        )
        
        # Register web research tool
        @self.agent.tool
        async def research_conversion_techniques(
            ctx: RunContext[AgentDependencies],
            topic: str,
            niche: str,
            focus_area: str
        ) -> str:
            """Research latest conversion optimization techniques"""
            # PATTERN: Use web_research tool with structured queries
            research_tool = WebResearchTool(ctx.deps.api_keys)
            
            # CRITICAL: Structure queries for maximum relevance
            queries = [
                f"{topic} conversion optimization {niche} 2024",
                f"best {focus_area} practices affiliate marketing",
                f"mobile first design {niche} psychology"
            ]
            
            findings = []
            for query in queries:
                try:
                    # GOTCHA: Rate limit web scraping to avoid blocks
                    await asyncio.sleep(1)
                    result = await research_tool.search(query, max_results=3)
                    findings.extend(result)
                except Exception as e:
                    # PATTERN: Graceful degradation
                    continue
            
            return self._synthesize_findings(findings, focus_area)

# Task 7: Website Generator Agent Implementation  
class WebsiteGeneratorAgent:
    """Primary agent that orchestrates website generation"""
    
    def __init__(self, model: str, deps: AgentDependencies):
        self.agent = Agent(
            model=model,
            deps_type=AgentDependencies,
            output_type=GeneratedWebsite,
            system_prompt="""You are an expert full-stack developer specializing in 
            creating high-converting affiliate marketing websites using React, Next.js,
            Tailwind CSS, and Vercel.
            
            Your expertise includes:
            - Modern React patterns with TypeScript
            - Next.js App Router and Server Components
            - Tailwind CSS utility-first design
            - Google Sheets API integration
            - SEO optimization and Core Web Vitals
            - Conversion rate optimization
            - Mobile-first responsive design
            - Vercel deployment optimization
            
            Generate production-ready, performant websites that achieve:
            - 90+ Lighthouse scores across all metrics
            - Sub-3 second loading times
            - Mobile-first responsive design
            - Accessibility compliance (WCAG 2.1)
            - SEO optimization for affiliate keywords"""
        )
        
        # Register research agent as tool
        @self.agent.tool
        async def get_ui_research(
            ctx: RunContext[AgentDependencies],
            niche: str,
            focus_area: str
        ) -> ResearchResult:
            """Get UI/UX research for specific niche and focus area"""
            # CRITICAL: Pass usage for token tracking in multi-agent calls
            research_agent = ResearchAgent(model="gpt-4", deps=ctx.deps)
            
            result = await research_agent.agent.run(
                f"Research {focus_area} best practices for {niche} affiliate marketing",
                deps=ctx.deps,
                usage=ctx.usage  # PATTERN from multi-agent docs
            )
            
            return result.data
        
        @self.agent.tool
        async def generate_react_component(
            ctx: RunContext[AgentDependencies],
            component_name: str,
            component_type: str,
            props_schema: Dict[str, Any],
            styling_requirements: str
        ) -> str:
            """Generate React component with TypeScript and Tailwind"""
            # PATTERN: Use template system with research-informed decisions
            template_gen = TemplateGenerator(ctx.deps.template_directory)
            
            # Get research for this component type
            research = await self.get_ui_research(
                ctx.deps.niche_context or "general",
                f"{component_type}_design"
            )
            
            # CRITICAL: Apply research findings to component generation
            component_code = template_gen.generate_component(
                name=component_name,
                type=component_type,
                props=props_schema,
                styling=styling_requirements,
                research_insights=research.recommendations
            )
            
            # GOTCHA: Validate TypeScript syntax before returning
            if not self._validate_typescript(component_code):
                raise ModelRetry("Generated TypeScript contains syntax errors")
            
            return component_code
        
        @self.agent.tool
        async def setup_google_sheets_integration(
            ctx: RunContext[AgentDependencies],
            sheets_config: GoogleSheetsConfig
        ) -> str:
            """Setup Google Sheets API integration"""
            # PATTERN: Generate API integration code with error handling
            sheets_tool = SheetsIntegrationTool()
            
            integration_code = await sheets_tool.generate_integration_code(
                config=sheets_config,
                output_format="nextjs_api_route"
            )
            
            # CRITICAL: Test API connection before finalizing
            try:
                await sheets_tool.test_connection(sheets_config)
            except Exception as e:
                raise ModelRetry(f"Google Sheets connection failed: {e}")
            
            return integration_code

# Task 8: CLI Implementation with Streaming
async def main_cli():
    """Main CLI interface with rich output and streaming"""
    console = Console()
    
    with console.status("[bold green]Initializing Website Generator..."):
        # Load configuration
        settings = Settings()
        deps = AgentDependencies(
            api_keys=settings.api_keys,
            output_directory=settings.output_dir,
            template_directory=settings.template_dir
        )
        
        # Initialize primary agent
        generator = WebsiteGeneratorAgent(
            model=settings.llm_model,
            deps=deps
        )
    
    # Interactive configuration
    request = await get_user_configuration(console)
    
    # Generate website with streaming output
    console.print("\n[bold blue]🚀 Generating your affiliate marketing website...\n")
    
    # PATTERN: Stream agent responses with tool visibility
    async for message in generator.agent.run_stream(
        f"Generate a complete affiliate marketing website for {request.niche} "
        f"niche with brand name '{request.brand_name}'. "
        f"Target audience: {request.target_audience}. "
        f"Optimize for: {', '.join(request.conversion_goals)}",
        deps=deps
    ):
        if isinstance(message, ModelResponse):
            console.print(f"🤖 {message.content}")
        elif isinstance(message, ToolCall):
            console.print(f"🛠 [dim]Using tool: {message.tool_name}[/dim]")
        elif isinstance(message, ToolReturn):
            console.print(f"✅ [dim]Tool completed: {message.tool_name}[/dim]")
    
    # Validate and deploy
    await validate_generated_website(deps.output_directory)
    await offer_vercel_deployment(request, console)
```

### Integration Points
```yaml
ENVIRONMENT:
  - add to: .env
  - vars: |
      # LLM Configuration
      LLM_PROVIDER=openai
      LLM_API_KEY=sk-...
      LLM_MODEL=gpt-4
      ANTHROPIC_API_KEY=ant-...
      
      # Google Sheets
      GOOGLE_SHEETS_API_KEY=AIza...
      GOOGLE_SHEETS_SERVICE_ACCOUNT=./credentials/service-account.json
      
      # Web Research
      SERPAPI_KEY=...
      BRAVE_SEARCH_KEY=...
      
      # Development
      OUTPUT_DIRECTORY=./generated
      TEMPLATE_DIRECTORY=./templates
      LOG_LEVEL=INFO

CONFIG:
  - Template Variables: All templates support Jinja2-style variable substitution
  - File Generation: Atomic writes with rollback on failure
  - Performance: Lighthouse CI integration for generated sites
  
DEPENDENCIES:
  - Update requirements.txt with:
    - pydantic-ai>=0.0.14
    - google-api-python-client
    - google-auth-httplib2  
    - jinja2
    - httpx
    - rich
    - pytest
    - pytest-asyncio
    - lighthouse
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
ruff check . --fix              # Auto-fix style issues
mypy .                          # Type checking
black .                         # Code formatting

# Expected: No errors. If errors, READ and fix.
```

### Level 2: Unit Tests
```python
# test_website_generator.py
async def test_website_generation():
    """Test complete website generation process"""
    deps = AgentDependencies(
        api_keys={"openai": "test-key"},
        output_directory="./test_output"
    )
    
    generator = WebsiteGeneratorAgent("test-model", deps)
    
    request = WebsiteGenerationRequest(
        niche=NicheType.TECH,
        brand_name="TechDeals Pro",
        target_audience="Tech enthusiasts looking for deals",
        sheets_config=GoogleSheetsConfig(sheet_id="test-sheet-id")
    )
    
    result = await generator.agent.run(
        "Generate tech affiliate marketing website",
        deps=deps
    )
    
    assert result.data.project_name == "TechDeals Pro"
    assert "package.json" in result.data.file_structure
    assert result.data.vercel_config is not None

async def test_research_agent():
    """Test research agent findings quality"""
    deps = AgentDependencies(api_keys={"openai": "test-key"})
    agent = ResearchAgent("test-model", deps)
    
    result = await agent.agent.run(
        "Research mobile-first design for fashion affiliate sites",
        deps=deps
    )
    
    assert result.data.confidence_score > 0.7
    assert len(result.data.findings) >= 3
    assert len(result.data.recommendations) >= 1

# test_file_generator.py
def test_react_component_generation():
    """Test React component generation with TypeScript"""
    generator = FileGenerator("./templates")
    
    component = generator.generate_component(
        name="ProductCard",
        type="product_display",
        props={"product": "Product", "onAddToCart": "() => void"},
        styling="conversion-optimized"
    )
    
    # Validate TypeScript syntax
    assert "interface" in component or "type" in component
    assert "export default" in component
    assert "className=" in component  # Tailwind classes
    
def test_google_sheets_integration():
    """Test Google Sheets API integration code generation"""
    tool = SheetsIntegrationTool()
    
    config = GoogleSheetsConfig(
        sheet_id="test-123",
        api_key="test-key"
    )
    
    code = tool.generate_integration_code(config, "nextjs_api_route")
    
    assert "async function handler" in code
    assert "GoogleAuth" in code or "sheets.spreadsheets" in code
    assert "res.status(200)" in code
```

```bash
# Run tests iteratively until passing:
pytest tests/ -v --cov=agents --cov=tools --cov-report=term-missing

# If failing: Debug specific test, fix code, re-run
```

### Level 3: Integration Test
```bash
# Test complete website generation
python cli.py

# Expected interaction:
# 🚀 Welcome to Affiliate Website Generator
# ? What niche are you targeting? Tech
# ? What's your brand name? TechDeals Pro  
# ? Target audience description? Tech enthusiasts seeking deals
# ? Google Sheets ID for products? 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
# 
# 🤖 Researching latest UI/UX trends for tech affiliate sites...
# 🛠 Using tool: research_conversion_techniques
# ✅ Research complete: Found 15 optimization techniques
# 
# 🤖 Generating React components with conversion optimization...
# 🛠 Using tool: generate_react_component (ProductCard)
# 🛠 Using tool: generate_react_component (Hero)
# ✅ Components generated successfully
#
# 🤖 Setting up Google Sheets integration...
# 🛠 Using tool: setup_google_sheets_integration
# ✅ API integration configured
#
# ✅ Website generated successfully!
# 📁 Output: ./generated/techdeals-pro/
# 🚀 Ready for Vercel deployment

# Test generated website
cd generated/techdeals-pro
npm install
npm run dev

# Expected: Website runs on localhost:3000 with no errors
# Lighthouse score should be 90+ across all metrics
```

### Level 4: Performance Validation
```bash
# Test generated website performance
cd generated/techdeals-pro
npm run build
npx lighthouse http://localhost:3000 --output=json --output-path=./lighthouse-report.json

# Expected performance targets:
# - Performance: 90+
# - Accessibility: 95+
# - Best Practices: 90+
# - SEO: 90+
# - First Contentful Paint: <2s
# - Largest Contentful Paint: <2.5s
# - Cumulative Layout Shift: <0.1

# Test mobile responsiveness
npx lighthouse http://localhost:3000 --emulated-form-factor=mobile --output=json

# Test Google Sheets integration
curl http://localhost:3000/api/products
# Expected: JSON array of products from Google Sheets
```

## Final Validation Checklist
- [ ] All tests pass: `pytest tests/ -v`
- [ ] No linting errors: `ruff check .`
- [ ] No type errors: `mypy .`
- [ ] Website Generator Agent creates complete React/Next.js projects
- [ ] Research Agent provides accurate UI/UX recommendations
- [ ] Generated websites achieve 90+ Lighthouse scores
- [ ] Google Sheets integration works with real data
- [ ] CLI provides rich, streaming output with tool visibility
- [ ] Generated websites are mobile-responsive
- [ ] SEO optimization is properly implemented
- [ ] Vercel deployment configurations are valid
- [ ] Error cases handled gracefully with user guidance
- [ ] Documentation includes setup and troubleshooting

---

## Anti-Patterns to Avoid
- ❌ Don't hardcode API keys - use environment variables
- ❌ Don't use sync functions in async agent context
- ❌ Don't skip TypeScript validation for generated React code
- ❌ Don't ignore responsive design requirements
- ❌ Don't forget to optimize images and performance
- ❌ Don't skip accessibility standards (WCAG 2.1)
- ❌ Don't generate websites without SEO optimization
- ❌ Don't use outdated React patterns or deprecated APIs
- ❌ Don't skip error handling in Google Sheets integration
- ❌ Don't forget to pass ctx.usage in multi-agent calls
- ❌ Don't commit generated websites to the main repository

## Confidence Score: 9/10

High confidence due to:
- Comprehensive research covering all required technologies (20+ documentation sources)
- Clear multi-agent architecture following Pydantic AI best practices
- Well-defined data models and validation strategies
- Proven patterns from existing PRP examples
- Extensive testing and validation gates
- Production-ready performance targets
- Clear file structure and implementation roadmap

Minor uncertainty on:
- Real-time web research API rate limits and reliability
- Google Sheets API authentication flow complexity in automated environment
- Vercel deployment automation edge cases

The comprehensive research foundation and clear implementation blueprint provide strong confidence for one-pass implementation success.