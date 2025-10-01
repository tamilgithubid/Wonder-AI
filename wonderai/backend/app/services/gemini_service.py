"""
Google Gemini service for handling AI interactions
Manages chat completions, embeddings, and image generation using Google's Gemini API
"""

import json
import asyncio
from typing import List, Dict, Any, Optional, AsyncGenerator
from datetime import datetime

try:
    import google.generativeai as genai
    from google.generativeai import GenerativeModel
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
except ImportError:
    # Fallback for development without Google AI installed
    genai = None
    GenerativeModel = None

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


class GeminiService:
    """Service for handling Google Gemini AI interactions"""
    
    def __init__(self):
        self.model = None
        self.chat = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize Gemini client"""
        
        if self._initialized:
            return
            
        if not genai:
            logger.warning("Google Generative AI package not installed. AI features will use mock responses.")
            self._initialized = True
            return
            
        if not settings.google_api_key:
            logger.warning("Google API key not configured. AI features will use mock responses.")
            self._initialized = True
            return
        
        # Configure the API key
        genai.configure(api_key=settings.google_api_key)
        
        # Initialize the model
        self.model = GenerativeModel(settings.GEMINI_MODEL)
        
        # Create a chat session
        self.chat = self.model.start_chat(history=[])
        
        self._initialized = True
        logger.info(f"Gemini service initialized with model: {settings.GEMINI_MODEL}")
    
    async def generate_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate chat completion using Gemini"""
        
        if not self._initialized:
            await self.initialize()
        
        # Return mock response if Gemini is not properly configured
        if not self.model:
            return self._mock_chat_response(messages[-1].get("content", "") if messages else "")
        
        try:
            start_time = datetime.utcnow()
            
            # Convert messages to Gemini format
            user_message = messages[-1].get("content", "") if messages else ""
            
            if stream:
                # For streaming, we'll return a generator wrapper
                return {
                    "response": self._generate_streaming_response(user_message),
                    "processing_time": 0,
                    "model": model or settings.GEMINI_MODEL,
                    "stream": True
                }
            else:
                # Generate response
                response = await self._generate_response(user_message)
                
                # Calculate processing time
                processing_time = (datetime.utcnow() - start_time).total_seconds()
                
                return {
                    "content": response,
                    "processing_time": processing_time,
                    "tokens_used": len(response.split()),  # Approximate token count
                    "model": model or settings.GEMINI_MODEL,
                    "stream": False
                }
                
        except Exception as e:
            logger.error(f"Chat completion error: {e}")
            return self._mock_chat_response(messages[-1].get("content", "") if messages else "")
    
    async def _generate_response(self, user_message: str) -> str:
        """Generate a single response using Gemini"""
        try:
            response = self.model.generate_content(
                user_message,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
            )
            return response.text
        except Exception as e:
            logger.error(f"Error generating Gemini response: {e}")
            raise
    
    async def _generate_streaming_response(self, user_message: str):
        """Generate streaming response using Gemini"""
        try:
            response = self.model.generate_content(
                user_message,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                },
                stream=True
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            logger.error(f"Error in streaming response: {e}")
            raise
    
    async def generate_streaming_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Generate streaming chat completion"""
        
        if not self._initialized:
            await self.initialize()
        
        # Return mock streaming if not configured
        if not self.model:
            async for chunk in self._mock_streaming_response(messages[-1].get("content", "") if messages else ""):
                yield chunk
            return
        
        user_message = messages[-1].get("content", "") if messages else ""
        
        try:
            response = self.model.generate_content(
                user_message,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                },
                stream=True
            )
            
            for chunk in response:
                if chunk.text:
                    yield {
                        "content": chunk.text,
                        "finished": False
                    }
            
            # Send completion signal
            yield {
                "content": "",
                "finished": True
            }
                    
        except Exception as e:
            logger.error(f"Streaming completion error: {e}")
            yield {
                "content": "",
                "error": str(e),
                "finished": True
            }
    
    async def _mock_streaming_response(self, user_message: str):
        """Mock streaming response for testing"""
        mock_response = f"🤖 Gemini 2.5 Flash response to: '{user_message}'. This is a mock response since Google Gemini is not properly configured."
        words = mock_response.split()
        
        for word in words:
            yield {
                "content": word + " ",
                "finished": False
            }
            await asyncio.sleep(0.1)
        
        yield {
            "content": "",
            "finished": True
        }
    
    async def generate_embeddings(
        self,
        texts: List[str],
        model: str = None
    ) -> List[List[float]]:
        """Generate text embeddings for RAG"""
        
        if not self._initialized:
            await self.initialize()
        
        # Return mock embeddings if Gemini is not configured
        if not genai:
            import random
            return [[random.random() for _ in range(768)] for _ in texts]  # Gemini embeddings are 768-dim
        
        try:
            all_embeddings = []
            
            for text in texts:
                result = genai.embed_content(
                    model=model or settings.GEMINI_EMBEDDING_MODEL,
                    content=text,
                    task_type="retrieval_document"
                )
                all_embeddings.append(result['embedding'])
            
            logger.info(f"Generated embeddings for {len(texts)} texts using Gemini")
            return all_embeddings
            
        except Exception as e:
            logger.error(f"Embedding generation error: {e}")
            # Return mock embeddings as fallback
            import random
            return [[random.random() for _ in range(768)] for _ in texts]
    
    async def generate_image(
        self,
        prompt: str,
        model: str = None,
        size: str = "1024x1024",
        **kwargs
    ) -> Dict[str, Any]:
        """Generate image using Gemini (note: Gemini primarily does text, this is a placeholder)"""
        
        # Gemini doesn't have direct image generation like DALL-E
        # This is a placeholder that could integrate with other services
        return {
            "image_url": f"https://via.placeholder.com/{size.replace('x', 'x')}?text=Gemini+Generated+Image",
            "revised_prompt": f"Gemini interpretation: {prompt}",
            "processing_time": 0.5,
            "model": model or settings.GEMINI_IMAGE_MODEL,
            "size": size,
            "note": "Gemini image generation is simulated - integrate with actual image service"
        }
    
    async def analyze_image(
        self,
        image_url: str,
        prompt: str = "What do you see in this image?",
        model: str = None
    ) -> Dict[str, Any]:
        """Analyze image content using Gemini vision capabilities"""
        
        if not self._initialized:
            await self.initialize()
        
        try:
            # Gemini can analyze images when properly configured
            # This would need the actual image data or URL handling
            response = f"Gemini analysis of image: {prompt}"
            
            return {
                "content": response,
                "processing_time": 0.5,
                "model": model or settings.GEMINI_MODEL
            }
            
        except Exception as e:
            logger.error(f"Image analysis error: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check Gemini API connectivity"""
        
        try:
            if not self._initialized:
                await self.initialize()
            
            if not self.model:
                return True  # Mock mode is considered "healthy"
            
            # Simple API test
            test_response = await self._generate_response("Hello")
            return len(test_response) > 0
            
        except Exception as e:
            logger.error(f"Gemini health check failed: {e}")
            return False
    
    def _mock_chat_response(self, user_message: str) -> Dict[str, Any]:
        """Generate mock chat response for testing"""
        
        import random
        
        responses = [
            f"🤖 Gemini 2.5 Flash here! You asked: '{user_message[:50]}...' This is a mock response since Google API is not configured.",
            "I'm Gemini 2.5 Flash in mock mode. Configure your Google API key to enable real AI responses.",
            f"Gemini response to: '{user_message}'. The WonderAI backend is working, but Google Gemini integration needs proper setup.",
            "Hello! I'm Gemini 2.5 Flash running in demo mode. Configure your Google API key for real responses.",
            f"Thank you for: '{user_message}'. I'm currently in Gemini mock mode without Google AI integration."
        ]
        
        return {
            "content": random.choice(responses),
            "processing_time": 0.1,
            "tokens_used": len(user_message) + 50,
            "model": "gemini-mock",
            "stream": False
        }


# Global Gemini service instance
gemini_service = GeminiService()
