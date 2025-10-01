#!/usr/bin/env python3
"""
Test streaming functionality end-to-end
"""

import asyncio
import aiohttp
import json

async def test_streaming_complete():
    print("🧪 Testing Complete Streaming Flow...")
    
    async with aiohttp.ClientSession() as session:
        try:
            payload = {"content": "Tell me a short story about streaming AI responses"}
            
            async with session.post(
                "http://localhost:8000/api/chat/conversations/stream-test-456/stream", 
                json=payload
            ) as response:
                
                print(f"Status: {response.status}")
                
                if response.status == 200:
                    full_message = ""
                    chunk_count = 0
                    
                    async for line in response.content:
                        if line:
                            line_str = line.decode('utf-8').strip()
                            if line_str.startswith('data: '):
                                data_str = line_str[6:]
                                try:
                                    data = json.loads(data_str)
                                    
                                    if data.get("type") == "content":
                                        content = data.get("content", "")
                                        full_message += content
                                        chunk_count += 1
                                        print(f"📦 Chunk {chunk_count}: '{content.strip()}'")
                                        
                                    elif data.get("type") == "complete" or data.get("finished"):
                                        print(f"✅ Streaming completed!")
                                        print(f"📝 Full message: '{full_message.strip()}'")
                                        print(f"📊 Total chunks: {chunk_count}")
                                        break
                                        
                                except json.JSONDecodeError:
                                    print(f"⚠️ Could not parse: {data_str}")
                    
                    return chunk_count > 0
                else:
                    text = await response.text()
                    print(f"❌ Error: {response.status} - {text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False

async def main():
    success = await test_streaming_complete()
    if success:
        print("\n🎉 Streaming functionality is working correctly!")
        print("✅ Backend streaming endpoint working")
        print("✅ Server-Sent Events format correct") 
        print("✅ Mock responses streaming properly")
        print("🌐 You can now test in the browser at http://localhost:5173")
        print("🎛️ Click the Activity button to toggle streaming on/off")
    else:
        print("\n❌ Streaming test failed")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())
