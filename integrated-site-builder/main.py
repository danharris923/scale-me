#!/usr/bin/env python3
"""
Integrated Site Builder - Automated Affiliate Marketing System

This script orchestrates the complete deployment of:
1. Scraper setup on GCP VM
2. Product data extraction
3. Website generation and deployment
4. Live API connection configuration
"""

import asyncio
import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from pydantic import BaseModel
from pydantic_ai import Agent

from scraper_integration.deployment_agent import ScraperDeploymentAgent
from site_integration.generator_agent import SiteGeneratorAgent
from shared.config import IntegratedConfig
from shared.utils import setup_logging, validate_environment


class DeploymentRequest(BaseModel):
    """Request model for integrated deployment."""
    niche: str
    brand_name: str
    target_audience: Optional[str] = None
    gcp_project_id: Optional[str] = None
    vercel_token: Optional[str] = None
    custom_config: Optional[Dict[str, Any]] = None


class IntegratedSystemAgent(Agent):
    """Main orchestration agent for the integrated system."""
    
    def __init__(self):
        super().__init__(
            model="claude-3-5-sonnet-latest",
            system_prompt="""You are an expert deployment orchestrator for affiliate marketing systems.
            
            Your role is to:
            1. Coordinate scraper deployment on GCP VM
            2. Ensure data extraction is working
            3. Generate optimized affiliate websites
            4. Configure live API connections
            5. Deploy to Vercel with proper environment setup
            6. Validate the complete integration
            
            Always provide detailed progress updates and handle errors gracefully.
            Ensure all components are working before marking deployment as complete."""
        )
        
        self.config = IntegratedConfig()
        self.scraper_agent = ScraperDeploymentAgent()
        self.site_agent = SiteGeneratorAgent()
        
    async def deploy_complete_system(self, request: DeploymentRequest) -> Dict[str, Any]:
        """Deploy the complete integrated affiliate marketing system."""
        
        logging.info(f"🚀 Starting integrated deployment for {request.brand_name} ({request.niche})")
        
        try:
            # Phase 1: Deploy Scraper Infrastructure
            logging.info("📊 Phase 1: Setting up scraper infrastructure...")
            scraper_result = await self.scraper_agent.deploy_scraper_system(
                niche=request.niche,
                gcp_project_id=request.gcp_project_id
            )
            
            if not scraper_result.get("success"):
                raise Exception(f"Scraper deployment failed: {scraper_result.get('error')}")
                
            # Phase 2: Validate Data Extraction
            logging.info("🔍 Phase 2: Validating product data extraction...")
            api_url = scraper_result["api_url"]
            products_count = await self._validate_scraper_data(api_url)
            
            if products_count < 5:
                logging.warning(f"Only {products_count} products found. Running additional scraping...")
                await self.scraper_agent.trigger_additional_scraping(api_url)
                
            # Phase 3: Generate Website
            logging.info("🌐 Phase 3: Generating affiliate website...")
            site_result = await self.site_agent.generate_affiliate_site(
                brand_name=request.brand_name,
                niche=request.niche,
                target_audience=request.target_audience or f"{request.niche} enthusiasts",
                scraper_api_url=api_url
            )
            
            if not site_result.get("success"):
                raise Exception(f"Site generation failed: {site_result.get('error')}")
                
            # Phase 4: Deploy to Vercel
            logging.info("🚀 Phase 4: Deploying to Vercel...")
            vercel_result = await self.site_agent.deploy_to_vercel(
                project_path=site_result["project_path"],
                api_url=api_url,
                vercel_token=request.vercel_token
            )
            
            # Phase 5: Final Validation
            logging.info("✅ Phase 5: Final system validation...")
            validation_result = await self._validate_complete_system(
                vercel_url=vercel_result["vercel_url"],
                api_url=api_url
            )
            
            # Compile final results
            deployment_summary = {
                "success": True,
                "brand_name": request.brand_name,
                "niche": request.niche,
                "scraper_api_url": api_url,
                "website_url": vercel_result["vercel_url"],
                "products_count": products_count,
                "validation": validation_result,
                "deployment_time": scraper_result.get("deployment_time", 0) + site_result.get("generation_time", 0),
                "next_steps": [
                    f"Visit your live site: {vercel_result['vercel_url']}",
                    f"Monitor API health: {api_url}/health", 
                    "Products will auto-update every 6 hours",
                    "Check deployment logs in ./logs/ directory"
                ]
            }
            
            # Save deployment record
            await self._save_deployment_record(deployment_summary)
            
            logging.info("🎉 Integrated deployment completed successfully!")
            return deployment_summary
            
        except Exception as e:
            logging.error(f"❌ Deployment failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "partial_results": getattr(self, '_partial_results', {})
            }
    
    async def _validate_scraper_data(self, api_url: str) -> int:
        """Validate that the scraper is returning product data."""
        import aiohttp
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{api_url}/products") as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("count", 0)
                    else:
                        logging.warning(f"API returned status {response.status}")
                        return 0
        except Exception as e:
            logging.error(f"Failed to validate scraper data: {e}")
            return 0
    
    async def _validate_complete_system(self, vercel_url: str, api_url: str) -> Dict[str, bool]:
        """Validate that the complete system is working end-to-end."""
        import aiohttp
        
        validation_results = {
            "scraper_api_healthy": False,
            "website_loads": False,
            "api_integration_working": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test scraper API health
                try:
                    async with session.get(f"{api_url}/health", timeout=10) as response:
                        validation_results["scraper_api_healthy"] = response.status == 200
                except:
                    pass
                
                # Test website loads
                try:
                    async with session.get(vercel_url, timeout=15) as response:
                        validation_results["website_loads"] = response.status == 200
                except:
                    pass
                
                # Test API integration through website
                try:
                    async with session.get(f"{vercel_url}/api/products", timeout=15) as response:
                        if response.status == 200:
                            data = await response.json()
                            validation_results["api_integration_working"] = data.get("count", 0) > 0
                except:
                    pass
                    
        except Exception as e:
            logging.error(f"System validation error: {e}")
        
        return validation_results
    
    async def _save_deployment_record(self, summary: Dict[str, Any]) -> None:
        """Save deployment record for future reference."""
        import json
        from datetime import datetime
        
        deployed_dir = Path("./deployed")
        deployed_dir.mkdir(exist_ok=True)
        
        brand_slug = summary["brand_name"].lower().replace(" ", "-")
        deployment_file = deployed_dir / f"{brand_slug}-deployment.json"
        
        record = {
            **summary,
            "deployed_at": datetime.now().isoformat(),
            "system_version": "1.0.0"
        }
        
        with open(deployment_file, "w") as f:
            json.dump(record, f, indent=2)
            
        logging.info(f"Deployment record saved to {deployment_file}")


async def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Deploy integrated affiliate marketing system")
    parser.add_argument("--niche", required=True, help="Product niche (e.g., tech, outdoor, fashion)")
    parser.add_argument("--brand", required=True, help="Brand name for the website")
    parser.add_argument("--audience", help="Target audience description")
    parser.add_argument("--gcp-project", help="GCP project ID")
    parser.add_argument("--vercel-token", help="Vercel deployment token")
    parser.add_argument("--config", help="Path to custom config file")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(log_level)
    
    # Validate environment
    if not validate_environment():
        logging.error("❌ Environment validation failed. Check your .env file.")
        sys.exit(1)
    
    # Create deployment request
    request = DeploymentRequest(
        niche=args.niche,
        brand_name=args.brand,
        target_audience=args.audience,
        gcp_project_id=args.gcp_project,
        vercel_token=args.vercel_token
    )
    
    # Initialize and run deployment
    agent = IntegratedSystemAgent()
    result = await agent.deploy_complete_system(request)
    
    if result["success"]:
        print("\n🎉 Deployment Successful!")
        print(f"🌐 Website: {result['website_url']}")
        print(f"📊 API: {result['scraper_api_url']}")
        print(f"📦 Products: {result['products_count']}")
        print("\n📋 Next Steps:")
        for step in result["next_steps"]:
            print(f"  • {step}")
    else:
        print(f"\n❌ Deployment Failed: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())