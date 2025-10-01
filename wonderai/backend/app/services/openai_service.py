"""
OpenAI service for handling AI interactions
Manages chat completions, embeddings, and image generation
"""

import json
import asyncio
from typing import List, Dict, Any, Optional, AsyncGenerator
from datetime import datetime

try:
    from openai import AsyncOpenAI
    from openai.types.chat import ChatCompletion, ChatCompletionChunk
except ImportError:
    # Fallback for development without OpenAI installed
    AsyncOpenAI = None
    ChatCompletion = None
    ChatCompletionChunk = None

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


class OpenAIService:
    """Service for handling OpenAI API interactions"""
    
    def __init__(self):
        self.client = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize OpenAI client"""
        
        if self._initialized:
            return
            
        if not AsyncOpenAI:
            logger.warning("OpenAI package not installed. AI features will use mock responses.")
            self._initialized = True
            return
            
        if not settings.openai_api_key:
            logger.warning("OpenAI API key not configured. AI features will use mock responses.")
            self._initialized = True
            return
        
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._initialized = True
        logger.info("OpenAI service initialized")
    
    async def generate_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate chat completion using OpenAI"""
        
        if not self._initialized:
            await self.initialize()
        
        # Return mock response if OpenAI is not properly configured
        if not self.client:
            return self._mock_chat_response(messages[-1].get("content", "") if messages else "")
        
        try:
            start_time = datetime.utcnow()
            
            # Prepare request parameters
            request_params = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "stream": stream,
                **kwargs
            }
            
            if max_tokens:
                request_params["max_tokens"] = max_tokens
            
            # Make API call
            response = await self.client.chat.completions.create(**request_params)
            
            # Calculate processing time
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            if stream:
                return {
                    "response": response,
                    "processing_time": processing_time,
                    "model": model,
                    "stream": True
                }
            else:
                return {
                    "content": response.choices[0].message.content,
                    "response": response,
                    "processing_time": processing_time,
                    "tokens_used": response.usage.total_tokens if response.usage else 0,
                    "model": model,
                    "stream": False
                }
                
        except Exception as e:
            logger.error(f"Chat completion error: {e}")
            raise
    
    async def generate_streaming_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Generate streaming chat completion"""
        
        completion_info = await self.generate_chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            **kwargs
        )
        
        response_stream = completion_info["response"]
        
        try:
            async for chunk in response_stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield {
                        "content": chunk.choices[0].delta.content,
                        "chunk": chunk,
                        "finished": False
                    }
                
                # Check if stream is finished
                if chunk.choices and chunk.choices[0].finish_reason:
                    yield {
                        "content": "",
                        "chunk": chunk,
                        "finished": True,
                        "finish_reason": chunk.choices[0].finish_reason
                    }
                    break
                    
        except Exception as e:
            logger.error(f"Streaming completion error: {e}")
            yield {
                "content": "",
                "error": str(e),
                "finished": True
            }
    
    async def generate_embeddings(
        self,
        texts: List[str],
        model: str = "text-embedding-3-small"
    ) -> List[List[float]]:
        """Generate text embeddings for RAG"""
        
        if not self._initialized:
            await self.initialize()
        
        # Return mock embeddings if OpenAI is not configured
        if not self.client:
            import random
            return [[random.random() for _ in range(1536)] for _ in texts]
        
        try:
            # Split large batches to avoid API limits
            batch_size = 100
            all_embeddings = []
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                
                response = await self.client.embeddings.create(
                    model=model,
                    input=batch
                )
                
                embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(embeddings)
                
                # Small delay between batches to respect rate limits
                if len(texts) > batch_size:
                    await asyncio.sleep(0.1)
            
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return all_embeddings
            
        except Exception as e:
            logger.error(f"Embedding generation error: {e}")
            raise
    
    async def generate_image(
        self,
        prompt: str,
        model: str = "dall-e-3",
        size: str = "1024x1024",
        quality: str = "standard",
        style: str = "natural"
    ) -> Dict[str, Any]:
        """Generate image using DALL-E"""
        
        if not self._initialized:
            await self.initialize()
        
        # Return mock image if OpenAI is not configured
        if not self.client:
            return {
                "image_url": f"https://via.placeholder.com/{size.replace('x', 'x')}?text=Mock+Image+for+{prompt[:20].replace(' ', '+')}",
                "revised_prompt": f"Mock image for: {prompt}",
                "processing_time": 0.5,
                "model": model,
                "size": size
            }
        
        try:
            start_time = datetime.utcnow()
            
            response = await self.client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                style=style,
                n=1
            )
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return {
                "image_url": response.data[0].url,
                "revised_prompt": getattr(response.data[0], 'revised_prompt', prompt),
                "processing_time": processing_time,
                "model": model,
                "size": size
            }
            
        except Exception as e:
            logger.error(f"Image generation error: {e}")
            raise
    
    async def analyze_image(
        self,
        image_url: str,
        prompt: str = "What do you see in this image?",
        model: str = "gpt-4o-mini"
    ) -> Dict[str, Any]:
        """Analyze image content using vision model"""
        
        if not self._initialized:
            await self.initialize()
        
        try:
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ]
            
            return await self.generate_chat_completion(
                messages=messages,
                model=model,
                max_tokens=500
            )
            
        except Exception as e:
            logger.error(f"Image analysis error: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check OpenAI API connectivity"""
        
        try:
            if not self._initialized:
                await self.initialize()
            
            if not self.client:
                return True  # Mock mode is considered "healthy"
            
            # Simple API test
            await self.client.models.list()
            return True
            
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            return False
    
    def _mock_chat_response(self, user_message: str) -> Dict[str, Any]:
        """Generate mock chat response for testing"""
        
        import random
        
        responses = [
            f"I understand you're asking about: '{user_message[:50]}...' This is a mock response since OpenAI is not configured.",
            "I'm a mock AI assistant. To enable real AI responses, please configure your OpenAI API key.",
            f"Mock response to: '{user_message}'. The WonderAI backend is working, but OpenAI integration needs configuration.",
            "Hello! I'm running in mock mode. Configure your OpenAI API key to enable real AI responses.",
            f"Thank you for your message: '{user_message}'. I'm currently in demo mode without OpenAI integration."
        ]
        
        return {
            "content": random.choice(responses),
            "response": None,
            "processing_time": 0.1,
            "tokens_used": len(user_message) + 50,
            "model": "mock-gpt",
            "stream": False
        }


# Global OpenAI service instance
openai_service = OpenAIService()
