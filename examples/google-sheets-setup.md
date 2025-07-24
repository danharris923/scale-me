# Google Sheets Setup Guide

This guide will help you set up Google Sheets for use with the Affiliate Marketing Website Generator.

## 🔗 Quick Setup (Public Sheet)

This is the easiest method for testing:

1. **Create your sheet**: https://sheets.new
2. **Import the template**: File → Import → Upload `sample-products-sheet.csv`
3. **Make it public**:
   - Share button → Change to "Anyone with the link can view"
   - Copy the sheet ID from the URL
4. **Use in the generator**: No API key needed!

## 🔐 Secure Setup (API Key)

For production use with access control:

### Step 1: Enable Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable the Google Sheets API:
   - Navigation menu → APIs & Services → Library
   - Search for "Google Sheets API"
   - Click Enable

### Step 2: Create API Credentials

1. Go to APIs & Services → Credentials
2. Click "+ CREATE CREDENTIALS" → API key
3. Copy the API key
4. (Optional) Restrict the key:
   - Click on the API key name
   - Under "API restrictions", select "Restrict key"
   - Choose "Google Sheets API"
   - Save

### Step 3: Set Sheet Permissions

1. Open your Google Sheet
2. Click Share
3. Under "General access", choose:
   - "Anyone with the link" → Viewer (for API key access)
   - OR add specific email if using service account

### Step 4: Configure the Generator

Add to your `.env` file:
```bash
GOOGLE_SHEETS_API_KEY=your_api_key_here
```

## 🤖 Advanced Setup (Service Account)

For maximum security and automation:

### Step 1: Create Service Account

1. In Google Cloud Console → IAM & Admin → Service Accounts
2. Click "Create Service Account"
3. Name it (e.g., "website-generator")
4. Create and download JSON key file

### Step 2: Share Sheet with Service Account

1. Open the JSON file and find the `client_email`
2. Share your Google Sheet with this email address (Viewer permission)

### Step 3: Configure the Generator

```bash
GOOGLE_SERVICE_ACCOUNT_FILE=path/to/service-account-key.json
```

## 📋 Sheet Structure Requirements

Your sheet must have these exact column headers (case-sensitive):

```
Name | Description | Price | Image URL | Affiliate URL | Category | Stock Status
```

### Column Details:

| Column | Type | Required | Example |
|--------|------|----------|---------|
| Name | Text | Yes | "iPhone 15 Pro" |
| Description | Text | No | "Latest Apple flagship..." |
| Price | Number | Yes | 999.99 |
| Image URL | URL | Yes | https://images.unsplash.com/... |
| Affiliate URL | URL | Yes | https://amzn.to/product |
| Category | Text | Yes | "Smartphones" |
| Stock Status | Enum | Yes | "in_stock", "low_stock", "out_of_stock" |

## 🔍 Finding Your Sheet ID

Your Google Sheets URL looks like:
```
https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit#gid=0
```

The Sheet ID is the long string between `/d/` and `/edit`.

Example:
- URL: `https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit`
- Sheet ID: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`

## 📊 Data Best Practices

### Images
- Use direct image URLs (not Google Drive links)
- Recommended size: 400x400px minimum
- Formats: JPG, PNG, WebP
- Consider using a CDN for performance

### Prices
- Use numbers only (no currency symbols)
- Decimal points for cents (e.g., 29.99)
- Keep consistent decimal places

### Categories
- Use consistent naming
- Avoid special characters
- Consider SEO-friendly names
- Group related products

### Stock Status
- Update regularly
- Use exactly: `in_stock`, `low_stock`, or `out_of_stock`
- Consider automation with Google Apps Script

## 🚀 Testing Your Setup

Run this test in the CLI:
```bash
python cli.py
# Select option to test Google Sheets integration
# Enter your Sheet ID
# Should see "✅ Google Sheets Integration Test PASSED"
```

## ⚠️ Common Issues

### "Permission denied"
- Check sheet sharing settings
- Verify API key has Sheets API enabled
- Ensure service account email has access

### "Invalid sheet ID"
- Double-check the ID from URL
- Remove any extra spaces
- Don't include the full URL

### "No data found"
- Check your range (default: "Sheet1!A:G")
- Ensure first row has headers
- Verify data starts in row 2

### "API quota exceeded"
- Google Sheets API has quotas
- Consider caching in production
- Upgrade to paid Google Cloud tier if needed

## 📚 Additional Resources

- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [API Quotas and Limits](https://developers.google.com/sheets/api/limits)
- [Service Account Best Practices](https://cloud.google.com/iam/docs/best-practices-for-using-service-accounts)