"""
Logging configuration for WonderAI backend
Using Loguru for structured, async-friendly logging
"""

import sys
from pathlib import Path
from loguru import logger
from app.core.config import settings


def setup_logging():
    """Configure application logging with Loguru"""
    
    # Remove default handler
    logger.remove()
    
    # Console handler with colors for development
    if settings.is_development:
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=settings.LOG_LEVEL,
            colorize=True,
        )
    else:
        # JSON format for production
        logger.add(
            sys.stdout,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
            level=settings.LOG_LEVEL,
            serialize=True,  # JSON output
        )
    
    # File handler for persistent logs
    log_dir = Path("./logs")
    log_dir.mkdir(exist_ok=True)
    
    logger.add(
        log_dir / "wonderai_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="1 month",
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        compression="gz",
    )
    
    # Error file handler
    logger.add(
        log_dir / "errors_{time:YYYY-MM-DD}.log",
        level="ERROR",
        rotation="1 day",
        retention="3 months",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message} | {exception}",
        compression="gz",
    )
    
    logger.info("🔧 Logging configured successfully")


def get_logger(name: str):
    """Get a logger instance with the given name"""
    return logger.bind(name=name)
