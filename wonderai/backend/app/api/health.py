"""
Health check API routes for WonderAI
Provides system health and status endpoints
"""

from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import get_db_session, openai_service, vector_service, db_service
from app.core.logging import get_logger
from app.core.config import get_settings

logger = get_logger(__name__)
router = APIRouter(prefix="/api", tags=["health"])
settings = get_settings()


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db_session)) -> Dict[str, Any]:
    """Main health check endpoint"""
    
    try:
        # Check database connectivity
        db_healthy = await db_service.health_check()
        
        # Check OpenAI service
        openai_healthy = await openai_service.health_check()
        
        # Check vector store
        vector_healthy = await vector_service.health_check()
        
        # Overall health status
        overall_healthy = all([db_healthy, openai_healthy, vector_healthy])
        
        return {
            "status": "healthy" if overall_healthy else "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "environment": settings.environment,
            "services": {
                "database": {
                    "status": "healthy" if db_healthy else "unhealthy",
                    "url": settings.database_url.split("@")[-1] if db_healthy else "unavailable"
                },
                "openai": {
                    "status": "healthy" if openai_healthy else "unhealthy",
                    "configured": bool(settings.openai_api_key)
                },
                "vector_store": {
                    "status": "healthy" if vector_healthy else "unhealthy",
                    "type": "faiss"
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }


@router.get("/health/database")
async def database_health_check(db: AsyncSession = Depends(get_db_session)) -> Dict[str, Any]:
    """Database-specific health check"""
    
    try:
        # Test database connection
        start_time = datetime.utcnow()
        healthy = await db_service.health_check()
        response_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "status": "healthy" if healthy else "unhealthy", 
            "response_time_ms": round(response_time * 1000, 2),
            "timestamp": datetime.utcnow().isoformat(),
            "connection_info": {
                "url": settings.database_url.split("@")[-1] if healthy else "unavailable",
                "pool_size": "auto",
                "echo": settings.debug
            }
        }
        
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@router.get("/health/openai")
async def openai_health_check() -> Dict[str, Any]:
    """OpenAI service health check"""
    
    try:
        start_time = datetime.utcnow()
        healthy = await openai_service.health_check()
        response_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "status": "healthy" if healthy else "unhealthy",
            "response_time_ms": round(response_time * 1000, 2),
            "timestamp": datetime.utcnow().isoformat(),
            "configuration": {
                "api_key_configured": bool(settings.openai_api_key),
                "default_model": "gpt-4o-mini",
                "embedding_model": "text-embedding-3-small"
            }
        }
        
    except Exception as e:
        logger.error(f"OpenAI health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@router.get("/health/vector")
async def vector_health_check() -> Dict[str, Any]:
    """Vector store health check"""
    
    try:
        start_time = datetime.utcnow()
        healthy = await vector_service.health_check()
        response_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Get vector store stats
        document_count = len(vector_service.documents) if vector_service._initialized else 0
        chunk_count = len(vector_service.chunks) if vector_service._initialized else 0
        
        return {
            "status": "healthy" if healthy else "unhealthy",
            "response_time_ms": round(response_time * 1000, 2),
            "timestamp": datetime.utcnow().isoformat(),
            "statistics": {
                "documents": document_count,
                "chunks": chunk_count,
                "dimension": vector_service.dimension if vector_service._initialized else 0,
                "index_type": "faiss.IndexFlatIP"
            }
        }
        
    except Exception as e:
        logger.error(f"Vector store health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@router.get("/status")
async def system_status() -> Dict[str, Any]:
    """Extended system status information"""
    
    try:
        return {
            "application": {
                "name": "WonderAI",
                "version": "1.0.0",
                "environment": settings.environment,
                "debug": settings.debug,
                "started_at": datetime.utcnow().isoformat()
            },
            "configuration": {
                "database_configured": bool(settings.database_url),
                "openai_configured": bool(settings.openai_api_key),
                "cors_enabled": True,
                "log_level": "INFO"
            },
            "features": {
                "chat": True,
                "image_generation": True,
                "image_analysis": True,
                "maps": True,
                "rag": True,
                "streaming": True
            },
            "limits": {
                "max_message_length": 10000,
                "max_conversation_history": 50,
                "max_rag_chunks": 5,
                "max_image_size": "2048x2048"
            }
        }
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return {
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
