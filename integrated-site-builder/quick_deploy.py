#!/usr/bin/env python3
"""
Quick Deploy Script - Generate and deploy outdoor adventure site
Connects to your existing GCS server and pushes to GitHub repo
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any
import requests


def check_server_status(server_url: str) -> Dict[str, Any]:
    """Check if the GCS server is running and has data."""
    try:
        print(f"🔍 Checking server status at {server_url}")
        
        # Check health
        health_response = requests.get(f"{server_url}/health", timeout=10)
        if health_response.status_code != 200:
            return {"success": False, "error": f"Health check failed: {health_response.status_code}"}
        
        # Check products
        products_response = requests.get(f"{server_url}/products", timeout=10)
        if products_response.status_code != 200:
            return {"success": False, "error": f"Products API failed: {products_response.status_code}"}
        
        data = products_response.json()
        products_count = data.get("count", 0)
        
        if products_count == 0:
            return {"success": False, "error": "No products found on server"}
        
        print(f"✅ Server is healthy with {products_count} products")
        return {
            "success": True, 
            "products_count": products_count,
            "sample_products": data.get("products", [])[:3]
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_site_files(server_url: str, output_dir: str) -> bool:
    """Create the site files for the outdoor adventure theme."""
    
    print("🎨 Generating outdoor adventure website files...")
    
    # Create directory structure
    site_dir = Path(output_dir)
    site_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    (site_dir / "pages" / "api").mkdir(parents=True, exist_ok=True)
    (site_dir / "pages" / "category").mkdir(parents=True, exist_ok=True)
    (site_dir / "components").mkdir(parents=True, exist_ok=True)
    (site_dir / "styles").mkdir(parents=True, exist_ok=True)
    (site_dir / "public").mkdir(parents=True, exist_ok=True)
    
    # Fetch sample products
    try:
        response = requests.get(f"{server_url}/products", timeout=10)
        sample_products = response.json().get("products", [])[:3] if response.status_code == 200 else []
    except:
        sample_products = []
    
    # Package.json
    package_json = {
        "name": "adventure-gear-pro",
        "version": "1.0.0",
        "description": "Outdoor adventure gear affiliate website",
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "lint": "next lint"
        },
        "dependencies": {
            "next": "^14.0.0",
            "react": "^18.0.0",
            "react-dom": "^18.0.0",
            "tailwindcss": "^3.3.0",
            "autoprefixer": "^10.4.16",
            "postcss": "^8.4.31"
        }
    }
    
    with open(site_dir / "package.json", "w") as f:
        json.dump(package_json, f, indent=2)
    
    # Main index page
    index_content = '''import Head from 'next/head'
import { useState, useEffect } from 'react'

export default function Home() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchProducts()
  }, [])

  const fetchProducts = async () => {
    try {
      const response = await fetch('/api/products')
      const data = await response.json()
      setProducts(data.products || [])
    } catch (error) {
      console.error('Error fetching products:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>Adventure Gear Pro - Quality Outdoor Equipment</title>
        <meta name="description" content="Find the best hiking, camping, and outdoor adventure gear. Quality equipment for your next outdoor expedition." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      {/* Navigation */}
      <nav className="bg-green-800 text-white shadow-lg">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold">Adventure Gear Pro</h1>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="bg-gradient-to-r from-green-800 to-green-600 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-6">Gear Up for Adventure</h1>
          <p className="text-xl mb-8">Quality outdoor equipment for hiking, camping, and exploring</p>
          <button className="bg-orange-500 hover:bg-orange-600 px-8 py-4 rounded-lg text-lg font-semibold">
            Shop Now
          </button>
        </div>
      </div>

      {/* Products Section */}
      <main className="container mx-auto px-4 py-12">
        <h2 className="text-3xl font-bold text-center mb-8">Featured Gear</h2>
        
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading outdoor gear...</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.map((product, index) => (
              <div key={index} className="bg-white rounded-lg shadow-lg overflow-hidden">
                <img 
                  src={product.image_url || '/placeholder.jpg'} 
                  alt={product.name}
                  className="w-full h-48 object-cover"
                />
                <div className="p-4">
                  <h3 className="font-semibold text-lg mb-2">{product.name}</h3>
                  <p className="text-gray-600 text-sm mb-3 line-clamp-2">{product.description}</p>
                  <div className="flex justify-between items-center">
                    <span className="text-2xl font-bold text-green-600">
                      ${typeof product.price === 'number' ? product.price.toFixed(2) : product.price}
                    </span>
                    <a 
                      href={product.affiliate_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded"
                    >
                      Shop Now
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8">
        <div className="container mx-auto px-4 text-center">
          <p>&copy; 2024 Adventure Gear Pro. All rights reserved.</p>
          <p className="mt-2 text-sm text-gray-400">
            We may earn a commission from purchases made through our affiliate links.
          </p>
        </div>
      </footer>
    </div>
  )
}'''
    
    with open(site_dir / "pages" / "index.js", "w") as f:
        f.write(index_content)
    
    # API route
    api_content = f'''export default async function handler(req, res) {{
  if (req.method !== 'GET') {{
    return res.status(405).json({{ error: 'Method not allowed' }})
  }}

  try {{
    const apiUrl = process.env.SCRAPER_API_URL || '{server_url}'
    
    const response = await fetch(`${{apiUrl}}/products`, {{
      headers: {{ 'Accept': 'application/json' }},
      timeout: 10000
    }})

    if (!response.ok) {{
      throw new Error(`API responded with status: ${{response.status}}`)
    }}

    const data = await response.json()
    
    if (!data.products || !Array.isArray(data.products)) {{
      throw new Error('Invalid data structure from API')
    }}

    data.fetched_at = new Date().toISOString()
    data.source = 'live-api'
    res.status(200).json(data)
    
  }} catch (error) {{
    console.error('Error fetching from GCS server:', error)
    
    // Fallback sample data
    const fallbackData = {{
      count: {len(sample_products) if sample_products else 0},
      products: {json.dumps(sample_products, indent=6) if sample_products else "[]"},
      source: 'fallback',
      error: error.message,
      fetched_at: new Date().toISOString()
    }}
    
    res.status(200).json(fallbackData)
  }}
}}'''
    
    with open(site_dir / "pages" / "api" / "products.js", "w") as f:
        f.write(api_content)
    
    # Global CSS
    css_content = '''@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  font-family: 'Arial', sans-serif;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}'''
    
    with open(site_dir / "styles" / "globals.css", "w") as f:
        f.write(css_content)
    
    # Tailwind config
    tailwind_config = '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}'''
    
    with open(site_dir / "tailwind.config.js", "w") as f:
        f.write(tailwind_config)
    
    # PostCSS config
    postcss_config = '''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}'''
    
    with open(site_dir / "postcss.config.js", "w") as f:
        f.write(postcss_config)
    
    # Environment example
    env_example = f'''SCRAPER_API_URL={server_url}
NEXT_PUBLIC_BRAND_NAME=Adventure Gear Pro'''
    
    with open(site_dir / ".env.example", "w") as f:
        f.write(env_example)
    
    # README
    readme_content = f'''# Adventure Gear Pro

Outdoor adventure gear affiliate website connected to live product data.

## 🚀 Features

- Live product data from {server_url}
- Responsive design optimized for mobile
- Fast loading Next.js architecture
- Conversion-optimized for affiliate marketing

## 🛠️ Development

```bash
npm install
npm run dev
```

## 🌐 Deployment

### Vercel
1. Connect repository to Vercel
2. Set environment variable: `SCRAPER_API_URL={server_url}`
3. Deploy

### Environment Variables
- `SCRAPER_API_URL`: Your GCS server URL

## 📊 Product Data

Connected to live scraper API for real-time outdoor gear from:
- Amazon outdoor equipment
- Cabela's hunting and camping gear

Products update automatically every 6 hours.'''
    
    with open(site_dir / "README.md", "w") as f:
        f.write(readme_content)
    
    print(f"✅ Generated website files in {output_dir}")
    return True


def setup_git_and_push(site_dir: str, repo_url: str) -> bool:
    """Set up git and push to the repository."""
    
    print(f"📡 Setting up git and pushing to {repo_url}")
    
    try:
        os.chdir(site_dir)
        
        # Initialize git if not already done
        if not Path(".git").exists():
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        
        # Add all files
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit
        commit_message = "🚀 Deploy Adventure Gear Pro - Outdoor affiliate site with live data"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # Force push to main
        print("🚀 Force pushing to GitHub...")
        subprocess.run(["git", "push", "origin", "main", "--force"], check=True)
        
        print("✅ Successfully pushed to GitHub!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main deployment function."""
    
    print("🏕️ Adventure Gear Pro - Quick Deploy Script")
    print("=" * 50)
    
    # Configuration
    server_url = input("Enter your GCS server URL (e.g., http://YOUR_IP:8000): ").strip()
    if not server_url:
        print("❌ Server URL is required")
        sys.exit(1)
    
    # Remove trailing slash
    server_url = server_url.rstrip('/')
    
    output_dir = "./adventure-gear-pro-site"
    repo_url = "https://github.com/danharris923/scale-me-testsite.git"
    
    # Step 1: Check server
    print("\n1. Checking GCS server...")
    server_status = check_server_status(server_url)
    if not server_status["success"]:
        print(f"❌ Server check failed: {server_status['error']}")
        print("Please ensure your GCS server is running and accessible.")
        sys.exit(1)
    
    # Step 2: Generate site
    print("\n2. Generating website...")
    if not create_site_files(server_url, output_dir):
        print("❌ Failed to generate website files")
        sys.exit(1)
    
    # Step 3: Git setup and push
    print("\n3. Deploying to GitHub...")
    if not setup_git_and_push(output_dir, repo_url):
        print("❌ Failed to push to GitHub")
        sys.exit(1)
    
    # Success!
    print("\n🎉 DEPLOYMENT COMPLETE!")
    print("=" * 50)
    print(f"✅ Website generated with {server_status['products_count']} products")
    print(f"✅ Pushed to: {repo_url}")
    print(f"✅ Connected to API: {server_url}")
    print("\n📋 Next Steps:")
    print("1. Check your GitHub repo for the updated files")
    print("2. Connect the repo to Vercel for automatic deployment")
    print(f"3. Set SCRAPER_API_URL environment variable to: {server_url}")
    print("4. Your live site will show real-time outdoor gear!")


if __name__ == "__main__":
    main()