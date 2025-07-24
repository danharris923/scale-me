# Example Files for Affiliate Marketing Website Generator

This directory contains example files to help you get started with the Affiliate Marketing Multi-Agent Website Generator.

## 📊 Google Sheets Template

### File: `sample-products-sheet.csv`

This CSV file shows the required structure for your Google Sheets product data. 

### Required Columns:

1. **Name** - Product name (required)
2. **Description** - Product description (optional but recommended)
3. **Price** - Product price in decimal format (required)
4. **Image URL** - Direct link to product image (required)
5. **Affiliate URL** - Your affiliate link for the product (required)
6. **Category** - Product category for organization (required)
7. **Stock Status** - One of: `in_stock`, `low_stock`, `out_of_stock` (required)

### Setting Up Your Google Sheet

1. **Create a new Google Sheet**
   - Go to [Google Sheets](https://sheets.google.com)
   - Create a new spreadsheet

2. **Import the template**
   - File → Import → Upload → Select `sample-products-sheet.csv`
   - Choose "Replace current sheet"

3. **Configure sharing**
   - Click "Share" button
   - Either:
     - Make it publicly readable (easier for testing)
     - OR use service account authentication (more secure)

4. **Get your Sheet ID**
   - Look at your sheet URL: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE/edit`
   - Copy the ID between `/d/` and `/edit`

5. **Use in the generator**
   ```bash
   python cli.py
   # When prompted for Google Sheets ID, paste your ID
   # Default range is "Sheet1!A:G" which includes all columns
   ```

### Example Products Included

The sample sheet includes 20 tech products across various categories:
- **Smartphones** - Latest iPhone and Samsung models
- **Laptops** - MacBook Pro, Dell XPS
- **Audio** - AirPods, Sony headphones, Bose earbuds
- **Gaming** - PlayStation 5, Xbox, Nintendo Switch
- **Accessories** - Keyboards, mice, webcams
- **And more!**

### Tips for Your Own Products

1. **Use high-quality images**
   - Minimum 400x400px recommended
   - Use Unsplash or product manufacturer images
   - Ensure images load quickly

2. **Write compelling descriptions**
   - Highlight key features
   - Keep it concise but informative
   - Include unique selling points

3. **Organize by categories**
   - Group similar products
   - Use consistent category names
   - Consider your target audience

4. **Track stock status**
   - Update regularly
   - Use automation if possible
   - Consider hiding out-of-stock items

5. **Optimize affiliate URLs**
   - Use URL shorteners if needed
   - Track clicks with UTM parameters
   - Ensure links are valid

### Image URL Sources

For demo purposes, you can use:
- **Unsplash**: `https://images.unsplash.com/photo-ID?w=400`
- **Placeholder**: `https://via.placeholder.com/400x400`
- **Your own CDN**: Upload to Cloudinary, AWS S3, etc.

### Affiliate URL Best Practices

- Always disclose affiliate relationships
- Use proper tracking parameters
- Test all links before publishing
- Consider using a link cloaking service
- Monitor for broken links regularly

## 🎨 Customization Examples

### Color Schemes
- **Tech Niche**: Blue (professional, trustworthy)
- **Fashion Niche**: Purple (creative, luxury)
- **Outdoor Gear**: Green (natural, adventure)

### Conversion Goals
- `maximize_clicks` - Focus on CTAs and urgency
- `build_trust` - Emphasize reviews and security
- `increase_engagement` - Interactive elements
- `improve_mobile_experience` - Mobile-first design
- `boost_seo_ranking` - Content and structure optimization

## 🚀 Quick Start Example

```bash
# 1. Import the sample CSV to Google Sheets
# 2. Get your Sheet ID
# 3. Run the generator
python cli.py

# Example inputs:
# Niche: 2 (Technology & Electronics)
# Brand Name: TechDeals Pro
# Target Audience: Tech enthusiasts looking for the latest gadgets
# Google Sheets ID: [your-sheet-id]
# Color Scheme: blue
# Conversion Goals: 1,2,3 (maximize clicks, build trust, increase engagement)
```

## 📝 Notes

- The sample data uses placeholder affiliate URLs (amzn.to/...)
- Replace with your actual affiliate links before deployment
- Stock status affects how products are displayed
- Categories are used for navigation and filtering
- Prices should not include currency symbols

For more examples and templates, visit the project documentation.