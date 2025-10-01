"""
Images API routes for WonderAI
Handles image generation and analysis endpoints
"""

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ValidationException
from app.services import get_db_session, openai_service
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/images", tags=["images"])


class ImageGenerationRequest(BaseModel):
    """Request model for image generation"""
    
    prompt: str
    model: str = "dall-e-3"
    size: str = "1024x1024"
    quality: str = "standard"
    style: str = "natural"
    user_id: Optional[str] = None


class ImageGenerationResponse(BaseModel):
    """Response model for image generation"""
    
    id: str
    image_url: str
    revised_prompt: str
    prompt: str
    model: str
    size: str
    processing_time: float
    created_at: datetime


class ImageAnalysisRequest(BaseModel):
    """Request model for image analysis"""
    
    image_url: str
    prompt: str = "What do you see in this image?"
    model: str = "gpt-4o-mini"
    user_id: Optional[str] = None


class ImageAnalysisResponse(BaseModel):
    """Response model for image analysis"""
    
    id: str
    analysis: str
    image_url: str
    prompt: str
    model: str
    processing_time: float
    tokens_used: int
    created_at: datetime


@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(
    request: ImageGenerationRequest,
    db: AsyncSession = Depends(get_db_session)
) -> ImageGenerationResponse:
    """Generate an image using DALL-E"""
    
    try:
        # Validate request
        if not request.prompt.strip():
            raise ValidationException("Prompt cannot be empty")
        
        if len(request.prompt) > 1000:
            raise ValidationException("Prompt too long (max 1000 characters)")
        
        # Validate image size
        valid_sizes = ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]
        if request.size not in valid_sizes:
            raise ValidationException(f"Invalid size. Must be one of: {valid_sizes}")
        
        # Generate image
        result = await openai_service.generate_image(
            prompt=request.prompt,
            model=request.model,
            size=request.size,
            quality=request.quality,
            style=request.style
        )
        
        # Create response
        response = ImageGenerationResponse(
            id=str(uuid.uuid4()),
            image_url=result["image_url"],
            revised_prompt=result["revised_prompt"],
            prompt=request.prompt,
            model=request.model,
            size=request.size,
            processing_time=result["processing_time"],
            created_at=datetime.utcnow()
        )
        
        logger.info(f"Generated image for prompt: {request.prompt[:50]}...")
        return response
        
    except ValidationException:
        raise
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate image")


@router.post("/analyze", response_model=ImageAnalysisResponse)
async def analyze_image(
    request: ImageAnalysisRequest,
    db: AsyncSession = Depends(get_db_session)
) -> ImageAnalysisResponse:
    """Analyze an image using vision model"""
    
    try:
        # Validate request
        if not request.image_url.strip():
            raise ValidationException("Image URL cannot be empty")
        
        if not request.prompt.strip():
            raise ValidationException("Analysis prompt cannot be empty")
        
        # Validate URL format (basic check)
        if not (request.image_url.startswith("http://") or request.image_url.startswith("https://")):
            raise ValidationException("Invalid image URL format")
        
        # Analyze image
        result = await openai_service.analyze_image(
            image_url=request.image_url,
            prompt=request.prompt,
            model=request.model
        )
        
        # Create response
        response = ImageAnalysisResponse(
            id=str(uuid.uuid4()),
            analysis=result["content"],
            image_url=request.image_url,
            prompt=request.prompt,
            model=request.model,
            processing_time=result["processing_time"],
            tokens_used=result.get("tokens_used", 0),
            created_at=datetime.utcnow()
        )
        
        logger.info(f"Analyzed image: {request.image_url[:50]}...")
        return response
        
    except ValidationException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing image: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze image")


@router.get("/models")
async def get_image_models() -> Dict[str, Any]:
    """Get available image generation models"""
    
    return {
        "generation_models": [
            {
                "id": "dall-e-3",
                "name": "DALL-E 3",
                "description": "Latest DALL-E model with improved quality and prompt adherence",
                "sizes": ["1024x1024", "1792x1024", "1024x1792"],
                "qualities": ["standard", "hd"],
                "styles": ["natural", "vivid"]
            },
            {
                "id": "dall-e-2",
                "name": "DALL-E 2", 
                "description": "Previous generation model",
                "sizes": ["256x256", "512x512", "1024x1024"],
                "qualities": ["standard"],
                "styles": ["natural"]
            }
        ],
        "analysis_models": [
            {
                "id": "gpt-4o-mini",
                "name": "GPT-4 Vision Mini",
                "description": "Efficient vision model for image analysis",
                "max_tokens": 4096
            },
            {
                "id": "gpt-4o",
                "name": "GPT-4 Vision",
                "description": "Advanced vision model with enhanced capabilities",
                "max_tokens": 4096
            }
        ]
    }


@router.get("/health")
async def image_health_check() -> Dict[str, Any]:
    """Health check for image generation service"""
    
    try:
        # Check OpenAI service health
        openai_healthy = await openai_service.health_check()
        
        return {
            "status": "healthy" if openai_healthy else "unhealthy",
            "openai_service": openai_healthy,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Image service health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
