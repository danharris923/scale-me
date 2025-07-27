# 🚀 Complete Deployment Guide - Scraper + Website

**COPY & PASTE COMMANDS FOR ZERO-BRAIN DEPLOYMENT**

This guide will get you from zero to a working affiliate marketing system in **10 minutes**.

---

## 📋 **Part 1: GCP VM Setup (Scraper Backend)**

### **Step 1.1: SSH into your GCP VM**

```bash
# Replace with your VM details
gcloud compute ssh affiliate-scraper --zone=us-central1-a
```

### **Step 1.2: Install Python and Dependencies**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11+ and pip
sudo apt install -y python3.11 python3.11-pip python3.11-venv curl git

# Make python3 point to python3.11
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Verify installation
python3 --version  # Should show Python 3.11+
```

### **Step 1.3: Clone the Scraper Repository**

```bash
# Clone your scraper repo
git clone https://github.com/danharris923/scrape-me.git
cd scrape-me

# List what we got
ls -la
```

### **Step 1.4: Install Python Dependencies**

```bash
# Install required packages
python3 -m pip install --user pydantic pydantic-settings python-dotenv
python3 -m pip install --user pydantic-ai playwright fastapi uvicorn
python3 -m pip install --user google-cloud-storage

# Install Playwright browsers
playwright install
```

### **Step 1.5: Create Configuration**

```bash
# Create environment file
cat > .env << 'EOF'
# Scraper Configuration
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-latest
LLM_API_KEY=

# Scraping Settings
SCRAPING_DELAY_SECONDS=2.0
MAX_RETRIES=3
QUALITY_THRESHOLD=0.7

# Directories
CONFIG_DIRECTORY=./config
OUTPUT_DIRECTORY=./output
STATE_DIRECTORY=./state
LOG_FILE=./scraper.log
LOG_LEVEL=INFO

# Optional: Google Cloud Storage
GCS_CREDENTIALS_PATH=
GCS_BUCKET_NAME=
EOF

# Create directories
mkdir -p output state
```

### **Step 1.6: Test the Simple Scraper**

```bash
# Run the scraper to generate fresh product data
python3 simple_scraper.py

# You should see output like:
# Starting Affiliate Product Scraper...
# Scraping outdoor-gear-site...
# Found: Coleman Dome Tent 6-Person - $71.99
# ...
# Scraping Complete!
# Total products scraped: 27

# Verify data was created
ls -la output/
cat output/outdoor-gear-site-products.json | head -20
```

### **Step 1.7: Start the API Server (Manual Method)**

```bash
# Start API server manually (for testing)
python3 api_server.py

# You should see:
# Starting Affiliate Scraper API on http://0.0.0.0:8000
# API will serve data from ./output directory
# INFO:     Uvicorn running on http://0.0.0.0:8000

# Leave this running and open a NEW terminal
# Test the API from another terminal:
curl http://localhost:8000/products
```

### **Step 1.8: Setup Automatic Startup (systemd Service)**

**Open a NEW SSH session** (keep API running in the first one for now):

```bash
# SSH into VM again
gcloud compute ssh affiliate-scraper --zone=us-central1-a

# Get your username and home directory
echo "Username: $(whoami)"
echo "Home: $HOME"
echo "Project: $HOME/scrape-me"

# Create systemd service file
sudo tee /etc/systemd/system/scraper-api.service > /dev/null << EOF
[Unit]
Description=Affiliate Scraper API Server
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=$(whoami)
Group=$(whoami)
WorkingDirectory=$HOME/scrape-me
Environment="PATH=/usr/bin:/usr/local/bin"
Environment="PYTHONPATH=$HOME/scrape-me"
ExecStart=/usr/bin/python3 $HOME/scrape-me/api_server.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Security settings
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$HOME/scrape-me/output

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable scraper-api
sudo systemctl start scraper-api

# Check if it's working
sudo systemctl status scraper-api

# View logs
sudo journalctl -u scraper-api -f
```

### **Step 1.9: Open Firewall Port**

**From your LOCAL machine** (not the GCP VM):

```bash
# Create firewall rule to allow port 8000
gcloud compute firewall-rules create allow-scraper-api \
  --allow tcp:8000 \
  --source-ranges 0.0.0.0/0 \
  --direction INGRESS \
  --priority 1000

# Get your VM's external IP
gcloud compute instances describe affiliate-scraper \
  --zone=us-central1-a \
  --format='value(networkInterfaces[0].accessConfigs[0].natIP)'

# Test from your local machine (replace with your actual IP)
curl http://YOUR_EXTERNAL_IP:8000/products
```

---

## 📋 **Part 2: Vercel Website Setup (Frontend)**

### **Step 2.1: Clone the Website Repository**

```bash
# On your LOCAL machine
git clone https://github.com/danharris923/scale-me-testsite.git
cd scale-me-testsite

# Install Node.js dependencies
npm install
```

### **Step 2.2: Configure API Connection**

```bash
# Run the setup script
npm run setup

# When prompted, enter your GCP VM's external IP:
# Example: http://34.130.183.243:8000

# This will:
# - Test the API connection
# - Update configuration files
# - Create .env.local file
```

**OR manually configure:**

```bash
# Create environment file
echo "SCRAPER_API_URL=http://YOUR_GCP_VM_IP:8000" > .env.local

# Replace YOUR_GCP_VM_IP with your actual IP from Step 1.9
```

### **Step 2.3: Test Locally**

```bash
# If you have a local server (optional)
npx serve .
# Open http://localhost:3000

# Or just deploy directly to Vercel
```

### **Step 2.4: Deploy to Vercel**

```bash
# Install Vercel CLI if you don't have it
npm install -g vercel

# Deploy
vercel --prod

# When prompted:
# ? Set up and deploy? [Y/n] y
# ? Which scope? [Your account]
# ? Link to existing project? [N/y] n
# ? What's your project's name? scale-me-testsite
# ? In which directory is your code located? ./

# Copy the deployment URL it gives you
```

### **Step 2.5: Set Vercel Environment Variable**

```bash
# Set environment variable in Vercel
vercel env add SCRAPER_API_URL production

# When prompted, enter: http://YOUR_GCP_VM_IP:8000

# Redeploy to use the new environment variable
vercel --prod
```

**OR use Vercel Dashboard:**

1. Go to https://vercel.com/dashboard
2. Click your project
3. Go to **Settings** → **Environment Variables**
4. Add:
   - **Name**: `SCRAPER_API_URL`
   - **Value**: `http://YOUR_GCP_VM_IP:8000`
   - **Environments**: All (Production, Preview, Development)
5. Click **Save**
6. Go to **Deployments** and redeploy

---

## 📋 **Part 3: Testing the Complete System**

### **Step 3.1: Test Scraper API**

```bash
# Replace with your actual GCP VM IP
curl http://YOUR_GCP_VM_IP:8000/health
curl http://YOUR_GCP_VM_IP:8000/products | head -20
```

### **Step 3.2: Test Website API Route**

```bash
# Test your Vercel deployment
curl https://your-site.vercel.app/api/products | head -20
```

### **Step 3.3: Visit Your Live Website**

Open your Vercel URL in browser: `https://your-site.vercel.app`

You should see **live product data** from your scraper!

---

## 📋 **Part 4: Automation & Maintenance**

### **Step 4.1: Schedule Regular Scraping**

**On your GCP VM:**

```bash
# Add to crontab for automatic scraping every 6 hours
crontab -e

# Add this line:
0 */6 * * * cd /home/$(whoami)/scrape-me && /usr/bin/python3 simple_scraper.py >> /home/$(whoami)/scraper-cron.log 2>&1

# View cron logs
tail -f ~/scraper-cron.log
```

### **Step 4.2: Monitor Services**

```bash
# Check API server status
sudo systemctl status scraper-api

# View API logs
sudo journalctl -u scraper-api -f

# Restart API if needed
sudo systemctl restart scraper-api

# Check what ports are open
sudo netstat -tlnp | grep 8000
```

### **Step 4.3: Update Product Data**

```bash
# Manually trigger scraping (on GCP VM)
cd ~/scrape-me
python3 simple_scraper.py

# Check new data
curl http://localhost:8000/products | python3 -c "import sys, json; print(f'Total: {json.load(sys.stdin)[\"count\"]} products')"
```

---

## 🚨 **Troubleshooting Commands**

### **GCP VM Issues:**

```bash
# Check if API server is running
ps aux | grep api_server

# Check if port is listening
sudo netstat -tlnp | grep 8000

# Restart everything
sudo systemctl restart scraper-api
sudo systemctl status scraper-api

# Check firewall
gcloud compute firewall-rules list | grep 8000

# Test internal API
curl http://localhost:8000/health
```

### **Vercel Issues:**

```bash
# Check deployments
vercel ls

# View deployment logs
vercel logs

# Redeploy
vercel --prod

# Check environment variables
vercel env ls
```

### **Data Issues:**

```bash
# Check scraper output
ls -la ~/scrape-me/output/
cat ~/scrape-me/output/*.json | head -10

# Run scraper manually
cd ~/scrape-me && python3 simple_scraper.py

# Test API data
curl http://YOUR_IP:8000/products | jq '.count'
```

---

## ✅ **Success Checklist**

- [ ] GCP VM can run `python3 simple_scraper.py` successfully
- [ ] API server responds to `curl http://YOUR_IP:8000/health`
- [ ] API returns products: `curl http://YOUR_IP:8000/products`
- [ ] Vercel site loads: `https://your-site.vercel.app`
- [ ] Vercel API works: `https://your-site.vercel.app/api/products`
- [ ] Website shows live product data (not fallback data)
- [ ] Firewall port 8000 is open on GCP
- [ ] systemd service starts on boot: `sudo systemctl status scraper-api`
- [ ] Cron job runs every 6 hours to update data

---

## 🎯 **Quick Commands Reference**

### **Get GCP VM IP:**
```bash
gcloud compute instances describe affiliate-scraper --zone=us-central1-a --format='value(networkInterfaces[0].accessConfigs[0].natIP)'
```

### **Test Everything:**
```bash
# Test scraper API
curl http://YOUR_IP:8000/products | jq '.count'

# Test website API
curl https://your-site.vercel.app/api/products | jq '.count'

# Check service status
sudo systemctl status scraper-api
```

### **Update Data:**
```bash
# On GCP VM
cd ~/scrape-me && python3 simple_scraper.py
```

### **View Logs:**
```bash
# API server logs
sudo journalctl -u scraper-api -f

# Cron scraping logs  
tail -f ~/scraper-cron.log
```

---

**🎉 Your affiliate marketing system is now LIVE!**

- **Scraper** generates fresh product data every 6 hours
- **API** serves this data at `http://YOUR_IP:8000`  
- **Website** displays live products at `https://your-site.vercel.app`

**Data Flow**: Scraper → JSON → API → Vercel → Users see fresh deals! 🚀