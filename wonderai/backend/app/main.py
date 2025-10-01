"""
WonderAI Backend - FastAPI Application
Modern AI-powered chatbot with RAG, image generation, and maps integration
"""

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.exceptions import setup_exception_handlers
from app.services import init_db, close_db
from app.api import chat_router, images_router, maps_router, health_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting WonderAI Backend...")
    
    # Setup logging
    setup_logging()
    
    # Initialize database
    logger.info("📁 Initializing database...")
    await init_db()
    
    # Initialize AI services
    logger.info("🤖 Initializing AI services...")
    # TODO: Initialize OpenAI, vector store, etc.
    
    logger.info("✅ WonderAI Backend started successfully!")
    logger.info(f"🌐 Environment: {settings.environment}")
    logger.info(f"🔧 Debug mode: {settings.debug}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down WonderAI Backend...")
    # TODO: Cleanup resources, close connections, etc.


# Create FastAPI application with modern configuration
app = FastAPI(
    title="WonderAI API",
    description="Modern AI-powered chatbot with RAG, image generation, and maps",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
    lifespan=lifespan,
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"]  # Configure as needed
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Setup exception handlers
setup_exception_handlers(app)

# Include API routes
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(images_router)
app.include_router(maps_router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to WonderAI API",
        "version": "1.0.0",
        "docs": "/docs" if settings.debug else "Documentation disabled in production",
        "status": "running",
        "environment": settings.environment,
    }


@app.get("/api/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "WonderAI API",
        "version": "1.0.0",
        "description": "Modern AI-powered chatbot with RAG, image generation, and maps",
        "features": [
            "Chat with AI assistant",
            "RAG-powered context awareness",
            "Image generation",
            "Interactive maps",
            "Real-time streaming",
            "Conversation history"
        ],
        "tech_stack": [
            "FastAPI",
            "SQLModel",
            "PostgreSQL", 
            "OpenAI",
            "FAISS",
            "WebSockets"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info",
        access_log=True,
    )
