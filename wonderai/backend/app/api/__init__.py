"""
API routes package for WonderAI application
Exports all API route modules
"""

from .chat import router as chat_router
from .images import router as images_router
from .maps import router as maps_router
from .health import router as health_router

__all__ = [
    "chat_router",
    "images_router", 
    "maps_router",
    "health_router"
]
