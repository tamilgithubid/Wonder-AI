#!/usr/bin/env python3
"""
Simple WonderAI Backend for Testing
Minimal FastAPI application to test basic functionality
"""

import os
import sys
from pathlib import Path

# Set environment variables
os.environ.setdefault("ENVIRONMENT", "development")
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("HOST", "0.0.0.0")
os.environ.setdefault("PORT", "8000")

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure FastAPI is installed: pip install fastapi uvicorn")
    sys.exit(1)

# Create simple FastAPI app
app = FastAPI(
    title="WonderAI API",
    description="AI-powered chatbot backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to WonderAI API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    """Simple health check"""
    return {
        "status": "healthy",
        "timestamp": "2024-10-01T17:00:00Z"
    }

@app.post("/api/chat/conversations")
async def create_conversation(conversation_data: dict):
    """Mock conversation creation"""
    return {
        "id": "conv-123",
        "title": conversation_data.get("title", "New Conversation"),
        "created_at": "2024-10-01T17:00:00Z"
    }

@app.get("/api/chat/conversations")
async def get_conversations():
    """Mock conversations list"""
    return [
        {
            "id": "conv-123",
            "title": "Sample Conversation",
            "created_at": "2024-10-01T17:00:00Z",
            "updated_at": "2024-10-01T17:00:00Z"
        }
    ]

@app.post("/api/chat/conversations/{conversation_id}/messages")
async def send_message(conversation_id: str, message_data: dict):
    """Message sending with direct Gemini AI integration"""
    
    user_content = message_data.get("content", "")
    
    try:
        import google.generativeai as genai
        
        # Configure API
        api_key = "AIzaSyAGu3LQ9E_9czmFxGVHYV4cpZajiIZm7Xg"
        genai.configure(api_key=api_key)
        
        # Create model and generate response
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(user_content)
        
        return {
            "id": "msg-user-123",
            "conversation_id": conversation_id,
            "content": user_content,
            "role": "user",
            "created_at": "2024-10-01T17:00:00Z",
            "ai_response": {
                "id": "msg-ai-123", 
                "content": response.text,
                "tokens_used": len(response.text.split())
            }
        }
        
    except Exception as e:
        return {
            "id": "msg-user-123",
            "conversation_id": conversation_id,
            "content": user_content,
            "role": "user", 
            "created_at": "2024-10-01T17:00:00Z",
            "ai_response": {
                "id": "msg-ai-123",
                "content": f"🤖 Gemini 2.5 Flash error: {str(e)}",
                "tokens_used": 0
            }
        }

@app.post("/api/chat/conversations/{conversation_id}/stream")
async def stream_message(conversation_id: str, message_data: dict):
    """Stream message responses using Server-Sent Events with direct Gemini integration"""
    from fastapi.responses import StreamingResponse
    import asyncio
    import json
    
    async def generate_stream():
        try:
            user_content = message_data.get("content", "") or message_data.get("message", "")
            
            if not user_content:
                user_content = "No message content received"
            
            # Try direct Gemini integration
            try:
                import google.generativeai as genai
                
                # Configure API
                api_key = "AIzaSyAGu3LQ9E_9czmFxGVHYV4cpZajiIZm7Xg"
                genai.configure(api_key=api_key)
                
                # Create model
                model = genai.GenerativeModel('gemini-2.0-flash-exp')
                
                # Generate streaming response
                response = model.generate_content(user_content, stream=True)
                
                for chunk in response:
                    if chunk.text:
                        data = {
                            "type": "content",
                            "content": chunk.text,
                            "finished": False
                        }
                        yield f"data: {json.dumps(data)}\n\n"
                
                # Send completion signal
                yield f"data: {json.dumps({'type': 'complete', 'finished': True})}\n\n"
                        
            except Exception as e:
                # Fallback to mock streaming
                mock_response = f"🤖 Gemini 2.5 Flash streaming response to: '{user_content}'. Error: {str(e)}"
                words = mock_response.split()
                
                for i, word in enumerate(words):
                    data = {
                        "type": "content", 
                        "content": word + (" " if i < len(words) - 1 else ""),
                        "finished": False
                    }
                    yield f"data: {json.dumps(data)}\n\n"
                    await asyncio.sleep(0.1)  # Simulate typing delay
                
                # Send completion signal
                yield f"data: {json.dumps({'type': 'complete', 'finished': True})}\n\n"
                
        except Exception as e:
            error_data = {
                "type": "error",
                "error": str(e),
                "finished": True
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.post("/api/images/generate")
async def generate_image(request_data: dict):
    """Mock image generation"""
    
    try:
        import sys
        sys.path.insert(0, "./app")
        from app.services.openai_service import openai_service
        
        result = await openai_service.generate_image(
            prompt=request_data.get("prompt", "A beautiful landscape"),
            size=request_data.get("size", "1024x1024")
        )
        
        return {
            "id": "img-123",
            "image_url": result["image_url"],
            "prompt": request_data.get("prompt", ""),
            "revised_prompt": result.get("revised_prompt", ""),
            "processing_time": result.get("processing_time", 0.5)
        }
        
    except Exception as e:
        return {
            "id": "img-123",
            "image_url": f"https://via.placeholder.com/1024x1024?text=Mock+Image+Error",
            "prompt": request_data.get("prompt", ""),
            "revised_prompt": f"Mock image (error: {str(e)})",
            "processing_time": 0.1
        }

if __name__ == "__main__":
    print("🚀 Starting Simple WonderAI Backend...")
    print("📡 API will be available at: http://localhost:8000")
    print("📚 API docs will be available at: http://localhost:8000/docs")
    
    uvicorn.run(
        "simple_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
