# 🔗 Scraper → Site Integration Setup

This guide shows how to connect your scraper API to your website for real-time product data.

## Architecture Overview

```
[Scraper (GCP VM)]          [Website (Vercel)]
    API Server      →→→       API Route
   Port 8000                /api/products
   ↓                           ↓
[Product JSONs]            [Frontend UI]
```

## 📝 Site-Side Changes

### 1. Update Environment Variable

For Vercel deployment, add your scraper API URL:

```bash
# In Vercel Dashboard > Settings > Environment Variables
SCRAPER_API_URL=http://YOUR_GCP_VM_EXTERNAL_IP:8000
```

For local development, create `.env.local`:
```bash
SCRAPER_API_URL=http://YOUR_GCP_VM_EXTERNAL_IP:8000
```

### 2. API Route Update (Already Done)

The `/testsite/api/products.js` has been updated to:
- Fetch from your GCP scraper API
- Fall back to sample data if API is down
- Use environment variable for API URL

## 🚀 GCP VM Setup

### 1. Get Your VM's External IP

```bash
# On your GCP VM
curl ifconfig.me
```

### 2. Open Firewall Port

```bash
# Allow API port through GCP firewall
gcloud compute firewall-rules create allow-scraper-api \
  --allow tcp:8000 \
  --source-ranges 0.0.0.0/0 \
  --target-tags scraper
```

### 3. Start the API Server

```bash
cd scrape-me
# Install dependencies
pip install -r requirements.txt

# Start the API server
python api_server.py
# Or use systemd service (see below)
```

### 4. Create systemd Service (Optional)

Create `/etc/systemd/system/affiliate-scraper-api.service`:

```ini
[Unit]
Description=Affiliate Scraper API Server
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/scrape-me
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python api_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable affiliate-scraper-api
sudo systemctl start affiliate-scraper-api
sudo systemctl status affiliate-scraper-api
```

## 🧪 Testing the Integration

### 1. Test Scraper API Directly

```bash
# From your local machine
curl http://YOUR_GCP_VM_IP:8000/products
```

### 2. Test Site API Route

```bash
# Local development
curl http://localhost:3000/api/products

# Vercel deployment
curl https://your-site.vercel.app/api/products
```

### 3. Check Frontend

Open your site and check the products table - it should now show live data from your scraper!

## 📊 Data Flow

1. **Scraper runs** → Saves JSON files to `./output/`
2. **API Server** → Serves these JSON files via REST endpoints
3. **Site API Route** → Fetches from scraper API
4. **Frontend** → Displays products in UI

## 🔍 Troubleshooting

### API Connection Issues

1. **Check firewall rules:**
   ```bash
   gcloud compute firewall-rules list
   ```

2. **Verify API is running:**
   ```bash
   curl http://localhost:8000/health  # On GCP VM
   ```

3. **Check CORS headers:**
   The scraper API allows all origins (`*`) in development

### No Products Showing

1. **Check scraper output directory:**
   ```bash
   ls -la scrape-me/output/
   ```

2. **Test API endpoints:**
   ```bash
   curl http://YOUR_GCP_VM_IP:8000/sites
   ```

3. **Check browser console** for errors

## 🎯 Next Steps

1. **Run scraper regularly** using cron:
   ```bash
   # Add to crontab
   0 */6 * * * cd /path/to/scrape-me && python main.py
   ```

2. **Monitor API health:**
   - Set up uptime monitoring
   - Add logging to track requests

3. **Optimize performance:**
   - Add caching layer
   - Use CDN for images
   - Implement pagination for large datasets

## 📱 API Endpoints Reference

- `GET /` - API documentation
- `GET /health` - Health check
- `GET /sites` - List available sites
- `GET /products` - Get all products
- `GET /products/{site_name}` - Get products from specific site

## 🔒 Security Considerations

1. **Restrict CORS** in production:
   ```python
   allow_origins=[
       "https://your-site.vercel.app",
       "https://your-custom-domain.com"
   ]
   ```

2. **Add API authentication** if needed
3. **Use HTTPS** with proper SSL certificates
4. **Rate limit** API requests

---

Your integration is now ready! The scraper provides real-time product data that your website can display to visitors. 🚀