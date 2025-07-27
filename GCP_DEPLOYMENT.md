# 🚀 GCP VM Deployment Guide

Your GCP VM IP: **34.130.183.243**

## Quick Setup Commands

Run these commands on your GCP VM:

```bash
# 1. SSH into your GCP VM
gcloud compute ssh YOUR_VM_NAME --zone=YOUR_ZONE

# 2. Clone/pull the scraper repository
cd ~
git clone https://github.com/YOUR_USERNAME/scale-me.git
# OR if already cloned:
cd scale-me && git pull

# 3. Navigate to scraper directory
cd scale-me/scraper

# 4. Install Python dependencies
python3 -m pip install -r requirements.txt

# 5. Create output directory if it doesn't exist
mkdir -p output

# 6. Test the API server
python3 api_server.py
```

## Open Firewall Port

Run this from your local machine (not the VM):

```bash
# Create firewall rule for port 8000
gcloud compute firewall-rules create allow-scraper-api \
  --allow tcp:8000 \
  --source-ranges 0.0.0.0/0 \
  --direction INGRESS \
  --priority 1000 \
  --network default \
  --action allow

# Or if you tagged your VM, use tags:
gcloud compute firewall-rules create allow-scraper-api \
  --allow tcp:8000 \
  --source-ranges 0.0.0.0/0 \
  --target-tags scraper
```

## Create systemd Service (Recommended)

On your GCP VM, create the service file:

```bash
# Create service file
sudo nano /etc/systemd/system/scraper-api.service
```

Add this content:

```ini
[Unit]
Description=Affiliate Scraper API Server
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/home/$USER/scale-me/scraper
Environment="PATH=/usr/local/bin:/usr/bin"
ExecStart=/usr/bin/python3 /home/$USER/scale-me/scraper/api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable scraper-api

# Start the service
sudo systemctl start scraper-api

# Check status
sudo systemctl status scraper-api

# View logs
sudo journalctl -u scraper-api -f
```

## Test the API

From your local machine:

```bash
# Test health endpoint
curl http://34.130.183.243:8000/health

# Test products endpoint
curl http://34.130.183.243:8000/products

# Test root endpoint
curl http://34.130.183.243:8000/
```

## Troubleshooting

### Port not accessible?

1. **Check if service is running:**
   ```bash
   sudo systemctl status scraper-api
   ps aux | grep api_server
   ```

2. **Check if port is listening:**
   ```bash
   sudo netstat -tlnp | grep 8000
   ```

3. **Check firewall rules:**
   ```bash
   gcloud compute firewall-rules list | grep 8000
   ```

4. **Check VM network tags:**
   ```bash
   gcloud compute instances describe YOUR_VM_NAME --zone=YOUR_ZONE | grep -A5 tags
   ```

### Service won't start?

1. **Check Python path:**
   ```bash
   which python3
   ```

2. **Test manually first:**
   ```bash
   cd /home/$USER/scale-me/scraper
   python3 api_server.py
   ```

3. **Check logs:**
   ```bash
   sudo journalctl -u scraper-api -n 50
   ```

## Running the Scraper

To populate data for the API:

```bash
cd ~/scale-me/scraper
python3 main.py
```

Or set up a cron job:

```bash
# Edit crontab
crontab -e

# Add this line to run every 6 hours
0 */6 * * * cd /home/$USER/scale-me/scraper && /usr/bin/python3 main.py >> /home/$USER/scraper.log 2>&1
```

## Security Notes

For production, consider:

1. **Use HTTPS** with Let's Encrypt
2. **Add authentication** to the API
3. **Restrict CORS** origins in `api_server.py`
4. **Set up monitoring** and alerts

---

Once the API is running on your GCP VM, your testsite will automatically fetch live product data! 🎉