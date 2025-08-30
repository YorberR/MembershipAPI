#!/usr/bin/env python3
"""Startup script for the FastAPI application."""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed."""
    try:
        import fastapi
        import sqlmodel
        import psycopg2
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists."""
    if Path(".env").exists():
        print("✅ Environment file found")
        return True
    else:
        print("❌ .env file not found")
        print("Please copy .env.example to .env and configure your settings")
        return False

def start_application():
    """Start the FastAPI application."""
    print("🚀 Starting FastAPI application...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped")

def main():
    """Main startup function."""
    print("FastAPI Professional Application Startup")
    print("=" * 40)
    
    if not check_requirements():
        sys.exit(1)
    
    if not check_env_file():
        sys.exit(1)
    
    print("\n📋 Application will be available at:")
    print("   - API: http://localhost:8000")
    print("   - Docs: http://localhost:8000/docs")
    print("   - Health: http://localhost:8000/health")
    print("\n🔐 Default credentials: admin / secret")
    print("\nPress Ctrl+C to stop the application\n")
    
    start_application()

if __name__ == "__main__":
    main()