#!/usr/bin/env python3
"""Build NextCV documentation locally."""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {cmd}")
        print(f"   Error: {e.stderr}")
        return False

def main():
    """Build the documentation."""
    print("🚀 Building NextCV Documentation")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("mkdocs.yml").exists():
        print("❌ Error: mkdocs.yml not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install mkdocs mkdocs-material mkdocs-gen-files mkdocs-literate-nav mkdocstrings[python] mkdocs-minify-plugin mkdocs-git-revision-date-localized-plugin", 
                      "Installing MkDocs dependencies"):
        print("💡 Tip: You might need to install dependencies manually or use a virtual environment")
        print("   Try: python -m venv venv && source venv/bin/activate && pip install ...")
        sys.exit(1)
    
    # Build documentation
    if not run_command("mkdocs build", "Building documentation"):
        sys.exit(1)
    
    # Check if site was created
    if Path("site").exists():
        print("✅ Documentation built successfully!")
        print("📁 Output directory: site/")
        print("🌐 To serve locally: mkdocs serve")
        print("🚀 To deploy: mkdocs gh-deploy")
    else:
        print("❌ Build failed - site directory not created")
        sys.exit(1)

if __name__ == "__main__":
    main()