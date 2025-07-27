# 🔧 Vercel Environment Variables Setup (Optional)

Since you have **no environment variables on Vercel**, your site will automatically use the hardcoded GCP IP: `http://34.130.183.243:8000`

## Current Setup (No Action Needed)

Your `/testsite/api/products.js` has this line:
```javascript
const SCRAPER_API = process.env.SCRAPER_API_URL || 'http://34.130.183.243:8000';
```

This means:
- ✅ **Vercel deployment**: Uses `http://34.130.183.243:8000` (hardcoded default)
- ✅ **Local development**: Uses value from `.env.local` if present, otherwise the hardcoded default

## If You Want to Add Environment Variables Later

### Option 1: Vercel Dashboard (Recommended)

1. Go to your project on [vercel.com](https://vercel.com)
2. Click on your `scale-me-testsite` project
3. Go to **Settings** → **Environment Variables**
4. Add new variable:
   - **Name**: `SCRAPER_API_URL`
   - **Value**: `http://34.130.183.243:8000`
   - **Environment**: Select all (Production, Preview, Development)
5. Click **Save**

### Option 2: Vercel CLI

```bash
# Install Vercel CLI if needed
npm i -g vercel

# Add environment variable
vercel env add SCRAPER_API_URL production
# When prompted, enter: http://34.130.183.243:8000
```

### Option 3: vercel.json (Not Recommended for Secrets)

Create `vercel.json` in testsite root:
```json
{
  "env": {
    "SCRAPER_API_URL": "http://34.130.183.243:8000"
  }
}
```

## Benefits of Using Environment Variables

1. **Easy Updates**: Change API URL without code changes
2. **Multiple Environments**: Different URLs for dev/staging/prod
3. **Security**: Hide internal IPs if needed (though this is public anyway)
4. **No Redeploys**: Update values without redeploying code

## Current Priority

**You don't need to set up environment variables right now!** 

The hardcoded default will work perfectly. Focus on:

1. ✅ Getting the scraper API running on your GCP VM
2. ✅ Opening port 8000 in GCP firewall
3. ✅ Testing the integration works

You can add environment variables later if you need more flexibility.

---

**TL;DR**: Your Vercel site will automatically use `http://34.130.183.243:8000` - no env setup needed! 🚀