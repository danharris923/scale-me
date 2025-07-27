#!/usr/bin/env python3
"""
Simplified main script for integrated site builder.
This version doesn't require complex agent imports.
"""

import json
import os
import sys
from pathlib import Path
import subprocess


def create_env_file():
    """Create .env file from example if it doesn't exist."""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if not env_path.exists() and env_example_path.exists():
        print("Creating .env file from .env.example...")
        with open(env_example_path, 'r') as src, open(env_path, 'w') as dst:
            dst.write(src.read())
        print("Please edit .env file with your actual configuration values.")
        return False
    return True


def main():
    """Main entry point for the integrated site builder."""
    
    print("🚀 Integrated Site Builder - Outdoor Adventure Edition")
    print("=" * 60)
    
    # Check for .env file
    if not create_env_file():
        print("\n⚠️  Please configure your .env file before running.")
        sys.exit(1)
    
    # For now, direct users to the quick deploy script
    print("\n✅ System is ready!")
    print("\n📋 Available Options:\n")
    
    print("1. Quick Deploy (Recommended)")
    print("   Run: python quick_deploy.py")
    print("   - Connects to your existing GCS server")
    print("   - Generates outdoor adventure site")
    print("   - Pushes to GitHub automatically")
    
    print("\n2. Manual Site Generation")
    print("   Edit config/outdoor-adventure.json for customization")
    print("   Then run quick_deploy.py with your settings")
    
    print("\n3. Custom Development")
    print("   - Modify templates in site-integration/")
    print("   - Add new themes in config/")
    print("   - Extend functionality as needed")
    
    print("\n🎯 Quick Start:")
    print("python quick_deploy.py")
    print("\nThis will generate and deploy your outdoor gear affiliate site!")


if __name__ == "__main__":
    main()