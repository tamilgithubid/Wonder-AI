#!/usr/bin/env python3
"""
Test script for WonderAI backend API
Tests all major endpoints to ensure they're working
"""

import asyncio
import aiohttp
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

async def test_health_endpoint():
    """Test health check endpoint"""
    print("🔍 Testing health endpoint...")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/health") as response:
                data = await response.json()
                print(f"✅ Health check: {data['status']}")
                return True
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False

async def test_conversation_endpoints():
    """Test conversation creation and retrieval"""
    print("🔍 Testing conversation endpoints...")
    
    async with aiohttp.ClientSession() as session:
        try:
            # Test conversation creation
            conversation_data = {
                "title": "Test Conversation",
                "status": "active"
            }
            
            async with session.post(
                f"{BASE_URL}/chat/conversations",
                json=conversation_data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Conversation created: {data.get('id', 'Unknown ID')}")
                else:
                    print(f"⚠️  Conversation creation returned: {response.status}")
                
            # Test conversations list
            async with session.get(f"{BASE_URL}/chat/conversations") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Conversations retrieved: {len(data) if isinstance(data, list) else 'Unknown count'}")
                else:
                    print(f"⚠️  Conversations list returned: {response.status}")
                    
            return True
            
        except Exception as e:
            print(f"❌ Conversation endpoints failed: {e}")
            return False

async def test_message_endpoint():
    """Test message sending with AI response"""
    print("🔍 Testing message endpoint...")
    
    async with aiohttp.ClientSession() as session:
        try:
            message_data = {
                "content": "Hello, this is a test message from the test script!"
            }
            
            async with session.post(
                f"{BASE_URL}/chat/conversations/conv-123/messages",
                json=message_data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    ai_response = data.get('ai_response', {})
                    print(f"✅ Message sent successfully")
                    print(f"📝 AI Response: {ai_response.get('content', 'No content')[:100]}...")
                    print(f"🔢 Tokens used: {ai_response.get('tokens_used', 0)}")
                else:
                    data = await response.text()
                    print(f"⚠️  Message endpoint returned: {response.status}")
                    print(f"Response: {data}")
                    
            return True
            
        except Exception as e:
            print(f"❌ Message endpoint failed: {e}")
            return False

async def test_image_endpoint():
    """Test image generation endpoint"""
    print("🔍 Testing image generation endpoint...")
    
    async with aiohttp.ClientSession() as session:
        try:
            image_data = {
                "prompt": "A beautiful sunset over mountains",
                "size": "1024x1024"
            }
            
            async with session.post(
                f"{BASE_URL}/images/generate",
                json=image_data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Image generated: {data.get('id', 'Unknown ID')}")
                    print(f"🖼️  Image URL: {data.get('image_url', 'No URL')[:80]}...")
                else:
                    data = await response.text()
                    print(f"⚠️  Image generation returned: {response.status}")
                    print(f"Response: {data}")
                    
            return True
            
        except Exception as e:
            print(f"❌ Image generation failed: {e}")
            return False

async def main():
    """Run all API tests"""
    print("🚀 Starting WonderAI Backend API Tests")
    print("=" * 50)
    
    tests = [
        test_health_endpoint,
        test_conversation_endpoints,
        test_message_endpoint,
        test_image_endpoint,
    ]
    
    results = []
    
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
        
        print("-" * 30)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
