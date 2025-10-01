#!/usr/bin/env python3
"""
Comprehensive test for streaming functionality
Tests both regular and streaming endpoints
"""

import asyncio
import aiohttp
import json
from typing import AsyncGenerator

async def test_regular_chat_endpoint():
    """Test the regular chat endpoint"""
    print("🧪 Testing regular chat endpoint...")
    
    async with aiohttp.ClientSession() as session:
        try:
            payload = {
                "conversationId": "test-conv-123",
                "content": "Hello! This is a test message for regular chat.",
                "messageType": "text"
            }
            
            async with session.post(
                "http://localhost:8000/api/chat/conversations/test-conv-123/messages", 
                json={"content": payload["content"], "messageType": payload["messageType"]}
            ) as response:
                
                print(f"   Status: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"   Response: {json.dumps(data, indent=2)}")
                    return True
                else:
                    text = await response.text()
                    print(f"   Error: {text}")
                    return False
                    
        except Exception as e:
            print(f"   Error: {e}")
            return False

async def test_streaming_endpoint():
    """Test the streaming endpoint"""
    print("🌊 Testing streaming endpoint...")
    
    async with aiohttp.ClientSession() as session:
        try:
            payload = {
                "message": "Tell me a story about AI and streaming responses."
            }
            
            async with session.post(
                "http://localhost:8000/api/chat/conversations/test-conv-123/stream", 
                json=payload
            ) as response:
                
                print(f"   Status: {response.status}")
                print(f"   Content-Type: {response.headers.get('content-type')}")
                
                if response.status == 200:
                    chunks_received = 0
                    async for line in response.content:
                        if line:
                            line_str = line.decode('utf-8').strip()
                            if line_str.startswith('data: '):
                                chunks_received += 1
                                data_str = line_str[6:]  # Remove 'data: ' prefix
                                if data_str == '[DONE]':
                                    print(f"   ✅ Stream completed - received {chunks_received} chunks")
                                    break
                                else:
                                    try:
                                        data = json.loads(data_str)
                                        print(f"   📦 Chunk {chunks_received}: {data.get('content', 'No content')[:50]}...")
                                    except json.JSONDecodeError:
                                        print(f"   📦 Raw chunk {chunks_received}: {data_str[:50]}...")
                    
                    return chunks_received > 0
                else:
                    text = await response.text()
                    print(f"   Error: {text}")
                    return False
                    
        except Exception as e:
            print(f"   Error: {e}")
            return False

async def test_health_endpoint():
    """Test the health endpoint"""
    print("❤️ Testing health endpoint...")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("http://localhost:8000/api/health") as response:
                print(f"   Status: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"   Health: {json.dumps(data, indent=2)}")
                    return True
                else:
                    text = await response.text()
                    print(f"   Error: {text}")
                    return False
                    
        except Exception as e:
            print(f"   Error: {e}")
            return False

async def main():
    """Run all streaming tests"""
    print("🚀 Starting Streaming Functionality Tests")
    print("=" * 50)
    
    # Test health first
    health_ok = await test_health_endpoint()
    print()
    
    # Test regular chat
    regular_ok = await test_regular_chat_endpoint()
    print()
    
    # Test streaming
    streaming_ok = await test_streaming_endpoint()
    print()
    
    # Summary
    print("📊 Test Results:")
    print(f"   Health Endpoint: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"   Regular Chat: {'✅ PASS' if regular_ok else '❌ FAIL'}")
    print(f"   Streaming: {'✅ PASS' if streaming_ok else '❌ FAIL'}")
    
    if all([health_ok, regular_ok, streaming_ok]):
        print("\n🎉 All streaming tests passed! Streaming functionality is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the backend server and endpoints.")
    
    return all([health_ok, regular_ok, streaming_ok])

if __name__ == "__main__":
    asyncio.run(main())
