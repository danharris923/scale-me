# 🚀 Integrated Site Builder - Automated Affiliate Marketing System

## Overview

This integrated system combines the **scraper** and **site builder** projects into a fully automated affiliate marketing pipeline:

1. **Scraper Agent** → Extracts product data using AI
2. **GCS API Server** → Serves live product data  
3. **Site Generator Agent** → Creates affiliate websites
4. **Auto-Deployment** → Deploys to Vercel with live data connection

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   SCRAPER       │    │   GCS SERVER     │    │  SITE BUILDER   │
│   (Auto-Run)    │───▶│   (Port 8000)    │───▶│   (Auto-Deploy) │
│                 │    │                  │    │                 │
│ • AI Scraping   │    │ • REST API       │    │ • AI Generated  │
│ • Product Data  │    │ • Live Updates   │    │ • React/Next.js │
│ • Context Eng.  │    │ • JSON Storage   │    │ • Auto Config   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Run integrated system
python main.py --niche "tech" --brand "TechDeals Pro"
```

This will:
- Set up the scraper on GCP VM
- Generate product data
- Create a custom affiliate website
- Deploy to Vercel with live API connection
- Configure automated updates

## Components

### `/scraper-integration/`
- Simplified scraper setup and deployment
- Auto-configuration for GCS server
- AI agents for intelligent product extraction

### `/site-integration/` 
- Website generator using site builder agents
- Automatic API connection configuration
- Vercel deployment automation

### `/shared/`
- Common utilities and configurations
- Integration helpers
- Deployment orchestration

## Environment Variables

```bash
# Required for full automation
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GCP_PROJECT_ID=your_gcp_project
VERCEL_TOKEN=your_vercel_token

# Optional customizations
SCRAPER_UPDATE_INTERVAL=6h
SITE_THEME=conversion-optimized
TARGET_NICHES=tech,outdoor,fashion
```

## Automation Features

✅ **One-Command Setup** - Deploy entire system with single command  
✅ **Auto-Configuration** - Smart detection of optimal settings  
✅ **Live Data Connection** - Websites automatically connect to scraper API  
✅ **Continuous Updates** - Products refresh every 6 hours  
✅ **Multi-Niche Support** - Generate sites for different product categories  
✅ **Performance Optimized** - 90+ Lighthouse scores out of the box  

## Generated Output

```
integrated-site-builder/
├── deployed/
│   ├── techdeals-pro/           # Generated affiliate site
│   │   ├── vercel-url.txt       # Live website URL
│   │   └── api-config.json      # API connection details
│   └── scraper-vm/              # GCP VM configuration
│       ├── external-ip.txt      # GCS server IP
│       └── service-status.txt   # Health check results
└── logs/
    ├── scraper-setup.log        # Scraper deployment logs
    ├── site-generation.log      # Website creation logs
    └── integration.log          # Full system logs
```

## Next Steps

1. **Run the integration**: `python main.py --niche "your-niche"`
2. **Monitor the dashboard**: Check logs and deployment status
3. **Customize as needed**: Edit configurations in `config/`
4. **Scale up**: Add more niches and product categories