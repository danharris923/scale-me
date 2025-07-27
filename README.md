# 🚀 Scale-Me - Integrated Affiliate Marketing System

Complete automation system combining **scraper** + **site builder** for outdoor adventure gear affiliate marketing.

## 🏗️ Project Structure

```
scale-me/
├── scraper/                    # Product scraping system (GCP VM)
├── site/                       # Website generator system  
├── integrated-site-builder/    # ⭐ NEW: Combined automation system
├── INTEGRATION_SETUP.md        # How projects work together
├── GCP_DEPLOYMENT.md          # GCS server deployment guide
└── DEPLOYMENT_GUIDE.md        # Complete deployment walkthrough
```

## 🎯 Quick Start - Integrated System

### For Outdoor Adventure Gear Sites:

```bash
cd integrated-site-builder
python quick_deploy.py
```

**What this does:**
1. ✅ Connects to your existing GCS server (Amazon + Cabela's data)
2. 🎨 Generates outdoor adventure themed website
3. 📡 Auto-pushes to GitHub for deployment
4. 🔄 Sets up live product data integration

### For Custom AI-Generated Sites:

```bash
cd integrated-site-builder
pip install -r requirements.txt
python main.py --niche "outdoor-adventure" --brand "Your Brand Name"
```

## 🔗 System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   SCRAPER       │    │   GCS SERVER     │    │  SITE BUILDER   │
│   (GCP VM)      │───▶│   (Port 8000)    │───▶│   (Vercel)      │
│                 │    │                  │    │                 │
│ • Amazon Data   │    │ • REST API       │    │ • React/Next.js │
│ • Cabela's Data │    │ • Live Updates   │    │ • AI Generated  │
│ • AI Agents     │    │ • JSON Storage   │    │ • Mobile Ready  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🏕️ Current Setup - Outdoor Adventure

**Live Data Sources:**
- ✅ Amazon outdoor equipment
- ✅ Cabela's hunting/camping gear
- ✅ Real-time price updates
- ✅ Product availability tracking

**Generated Sites Feature:**
- 🎨 Outdoor adventure theme (green/earth tones)
- 📱 Mobile-responsive design
- ⚡ 90+ Lighthouse performance scores
- 🔄 Auto-updates every 6 hours
- 💰 Conversion-optimized layouts

## 📊 Individual Components

### Scraper System (`/scraper/`)
- **Purpose**: Extract product data using AI agents
- **Deployment**: GCP VM with API server
- **Data**: Amazon + Cabela's outdoor gear
- **Output**: JSON files served via REST API

### Site Builder (`/site/`)  
- **Purpose**: Generate affiliate marketing websites
- **Technology**: React/Next.js with AI agents
- **Features**: Multi-niche support, SEO optimization
- **Deployment**: Vercel with Google Sheets integration

### Integrated Builder (`/integrated-site-builder/`) ⭐
- **Purpose**: Complete automation combining both systems
- **Features**: One-command deployment, GitHub integration
- **Specialization**: Outdoor adventure gear optimization
- **Output**: Production-ready affiliate sites

## 🚀 Deployment Options

### Option 1: Quick Deploy (Recommended)
```bash
cd integrated-site-builder
python quick_deploy.py
# Enter your GCS server URL when prompted
```

### Option 2: Manual Component Setup
1. **Set up scraper** (see GCP_DEPLOYMENT.md)
2. **Generate site** (see site/README.md)  
3. **Connect integration** (see INTEGRATION_SETUP.md)

### Option 3: Full AI Generation
```bash
cd integrated-site-builder
python main.py --niche "outdoor" --brand "Adventure Pro"
```

## 📋 Environment Setup

```bash
# Required for integrated system
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GCS_SERVER_URL=http://YOUR_SERVER_IP:8000

# Optional for full automation  
VERCEL_TOKEN=your_vercel_token
GCP_PROJECT_ID=your_gcp_project
```

## 🎯 Current Status

✅ **GCS Server Running** - Amazon + Cabela's data live  
✅ **Integrated Builder Ready** - Outdoor adventure optimized  
✅ **GitHub Integration** - Auto-push to scale-me-testsite  
🚀 **Ready for Deployment** - One command away from live site  

## 📖 Documentation

- **INTEGRATION_SETUP.md** - How scraper + site work together
- **GCP_DEPLOYMENT.md** - Deploy scraper to Google Cloud  
- **DEPLOYMENT_GUIDE.md** - Complete step-by-step guide
- **VERCEL_ENV_SETUP.md** - Environment variable configuration

## 🏕️ Perfect for Outdoor Gear

This system is optimized for outdoor adventure affiliate marketing:
- **Hiking gear** from Amazon
- **Camping equipment** from Cabela's  
- **Seasonal promotions** and deal alerts
- **Mobile-first** for on-the-go adventurers
- **High-converting** product displays

---

**Ready to launch your outdoor gear affiliate empire? Start with the integrated site builder!** 🏔️