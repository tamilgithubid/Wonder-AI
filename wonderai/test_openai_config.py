#!/usr/bin/env python3
"""
OpenAI Configuration Test Script
Tests whether OpenAI API key is properly configured and working
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the app directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir / "app"))

async def test_openai_configuration():
    """Test OpenAI configuration and functionality"""
    print("🔧 Testing OpenAI Configuration...")
    print("=" * 50)
    
    try:
        # Import configuration
        from core.config import get_settings
        settings = get_settings()
        
        print(f"📋 Current Configuration:")
        print(f"   OpenAI API Key: {'✅ Configured' if settings.openai_api_key else '❌ Not configured'}")
        print(f"   OpenAI Model: {settings.OPENAI_MODEL}")
        print(f"   Embedding Model: {settings.OPENAI_EMBEDDING_MODEL}")
        print(f"   Environment: {settings.ENVIRONMENT}")
        
        if not settings.openai_api_key:
            print("\n❌ OpenAI API Key not found!")
            print("📝 To configure:")
            print("   1. Get API key from https://platform.openai.com/api-keys")
            print("   2. Create .env file in backend directory")
            print("   3. Add: OPENAI_API_KEY=sk-your-key-here")
            print("   4. Restart the backend server")
            return False
        
        # Test OpenAI service
        print(f"\n🧪 Testing OpenAI Service...")
        
        from services.openai_service import openai_service
        
        # Initialize service
        await openai_service.initialize()
        
        # Test health check
        is_healthy = await openai_service.health_check()
        print(f"   Health Check: {'✅ Passed' if is_healthy else '❌ Failed'}")
        
        if not openai_service.client:
            print("   Status: 🔄 Running in mock mode (API key not configured)")
            return False
        
        # Test basic chat completion
        print(f"   Testing chat completion...")
        
        messages = [{"role": "user", "content": "Say 'Hello from OpenAI!' to confirm the API is working."}]
        result = await openai_service.generate_chat_completion(messages, max_tokens=50)
        
        if result and result.get('content'):
            print(f"   Chat Test: ✅ Success")
            print(f"   Response: {result['content'][:100]}...")
            print(f"   Model Used: {result.get('model', 'unknown')}")
            print(f"   Tokens: {result.get('tokens_used', 0)}")
        else:
            print(f"   Chat Test: ❌ Failed - No response content")
            return False
            
        # Test embeddings
        print(f"   Testing embeddings...")
        try:
            embeddings = await openai_service.generate_embeddings(["Test text for embeddings"])
            if embeddings and len(embeddings[0]) > 0:
                print(f"   Embeddings Test: ✅ Success (dimension: {len(embeddings[0])})")
            else:
                print(f"   Embeddings Test: ❌ Failed")
        except Exception as e:
            print(f"   Embeddings Test: ⚠️ Error: {e}")
        
        print(f"\n🎉 OpenAI Configuration Test: ✅ PASSED")
        print(f"   Your OpenAI API key is working correctly!")
        print(f"   Real AI responses are now enabled in WonderAI.")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print(f"   Make sure you're running this from the wonderai directory")
        return False
    except Exception as e:
        print(f"❌ Configuration Error: {e}")
        return False

def show_quick_setup():
    """Show quick setup instructions"""
    print("\n" + "=" * 60)
    print("🚀 QUICK SETUP GUIDE")
    print("=" * 60)
    print()
    print("1️⃣ Get OpenAI API Key:")
    print("   Visit: https://platform.openai.com/api-keys")
    print("   Create new secret key (starts with 'sk-')")
    print()
    print("2️⃣ Configure Backend:")
    print("   cd /home/hire/Desktop/AI_CHAT_BOT/wonderai/backend")
    print("   cp .env.example .env")
    print("   nano .env  # Edit and add your API key")
    print()
    print("3️⃣ Restart Backend:")
    print("   python simple_server.py")
    print()
    print("4️⃣ Test in Browser:")
    print("   Open: http://localhost:5173")
    print("   Send a message and see real AI responses!")
    print()

async def main():
    """Main test function"""
    success = await test_openai_configuration()
    
    if not success:
        show_quick_setup()
    
    return success

if __name__ == "__main__":
    asyncio.run(main())
