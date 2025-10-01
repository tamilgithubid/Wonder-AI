#!/usr/bin/env python3
"""
Simple direct Gemini API test
"""

import asyncio
import os

async def test_gemini_direct():
    print("🧪 Testing Gemini API directly...")
    
    # Test 1: Check if package is available
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI package is available")
    except ImportError as e:
        print(f"❌ Google Generative AI package not found: {e}")
        return
    
    # Test 2: Configure with API key
    api_key = "AIzaSyAGu3LQ9E_9czmFxGVHYV4cpZajiIZm7Xg"
    genai.configure(api_key=api_key)
    print(f"🔑 API Key configured: {api_key[:10]}...{api_key[-4:]}")
    
    # Test 3: Create model
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        print("✅ Model created successfully")
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        return
    
    # Test 4: Simple generation
    try:
        response = model.generate_content("Say 'Hello from Gemini 2.5 Flash!' in one sentence.")
        print("✅ Simple generation successful!")
        print(f"📝 Response: {response.text}")
    except Exception as e:
        print(f"❌ Simple generation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 5: Streaming generation
    try:
        print("🔄 Testing streaming...")
        response = model.generate_content("Count from 1 to 5, one number per sentence.", stream=True)
        chunks = []
        for chunk in response:
            if chunk.text:
                chunks.append(chunk.text)
                print(f"📝 Chunk: {chunk.text.strip()}")
        
        print(f"✅ Streaming successful! Received {len(chunks)} chunks")
    except Exception as e:
        print(f"❌ Streaming failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_gemini_direct())
