#!/usr/bin/env python3
"""
WonderAI Backend Startup Script
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the app directory to the Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

# Set environment variables for testing
os.environ.setdefault("ENVIRONMENT", "development")
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./wonderai.db")
os.environ.setdefault("HOST", "0.0.0.0")
os.environ.setdefault("PORT", "8000")

# Optional: Set OpenAI API key if available
# os.environ.setdefault("OPENAI_API_KEY", "your-openai-api-key-here")

def main():
    """Main startup function"""
    try:
        # Import and run the FastAPI application
        import uvicorn
        from app.main import app
        
        print("🚀 Starting WonderAI Backend...")
        print("📡 API will be available at: http://localhost:8000")
        print("📚 API docs will be available at: http://localhost:8000/docs")
        print("🔄 Auto-reload enabled for development")
        print("---")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True,
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down WonderAI Backend...")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Startup error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
