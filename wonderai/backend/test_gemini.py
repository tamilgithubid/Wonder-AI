#!/usr/bin/env python3
"""
Test Gemini integration directly
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, "./app")

async def test_gemini():
    print("🧪 Testing Gemini integration...")
    
    # Test 1: Check if google.generativeai is installed
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI package is available")
    except ImportError as e:
        print(f"❌ Google Generative AI package not found: {e}")
        return
    
    # Test 2: Check environment variables
    from app.core.config import get_settings
    settings = get_settings()
    
    print(f"🔑 Google API Key configured: {'Yes' if settings.google_api_key else 'No'}")
    print(f"🔑 API Key preview: {settings.google_api_key[:10]}...{settings.google_api_key[-4:] if settings.google_api_key else 'None'}")
    print(f"🤖 Gemini Model: {settings.GEMINI_MODEL}")
    
    # Test 3: Try to initialize Gemini service
    try:
        from app.services.gemini_service import gemini_service
        await gemini_service.initialize()
        print(f"✅ Gemini service initialized: {gemini_service._initialized}")
        print(f"🤖 Model available: {'Yes' if gemini_service.model else 'No'}")
    except Exception as e:
        print(f"❌ Gemini service initialization failed: {e}")
        return
    
    # Test 4: Try a simple API call
    try:
        response = await gemini_service.generate_chat_completion([
            {"role": "user", "content": "Say 'Hello from Gemini!' in one sentence."}
        ])
        print(f"✅ Gemini API call successful!")
        print(f"📝 Response: {response.get('content', 'No content')}")
        print(f"⏱️ Processing time: {response.get('processing_time', 0)}s")
    except Exception as e:
        print(f"❌ Gemini API call failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 5: Try streaming
    try:
        print("🔄 Testing streaming...")
        stream_chunks = []
        async for chunk in gemini_service.generate_streaming_completion([
            {"role": "user", "content": "Count from 1 to 3 in one sentence."}
        ]):
            stream_chunks.append(chunk)
            if chunk.get("finished"):
                break
        
        full_response = "".join([chunk.get("content", "") for chunk in stream_chunks if not chunk.get("finished")])
        print(f"✅ Streaming successful! Received {len(stream_chunks)} chunks")
        print(f"📝 Streamed response: {full_response}")
    except Exception as e:
        print(f"❌ Streaming failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini())
