"""
Database service for managing async database operations
Handles connection, sessions, and CRUD operations
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel, create_engine

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


class DatabaseService:
    """Database service for managing async connections and sessions"""
    
    def __init__(self):
        self.engine = None
        self.async_session = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize the database connection and session maker"""
        
        if self._initialized:
            return
            
        try:
            # Create async engine with connection pool settings
            self.engine = create_async_engine(
                settings.database_url,
                echo=settings.debug,
                poolclass=NullPool if settings.environment == "test" else None,
                pool_pre_ping=True,
                pool_recycle=3600,  # Recycle connections after 1 hour
                connect_args={
                    "server_settings": {
                        "jit": "off"  # Disable JIT for better performance with small queries
                    }
                } if "postgresql" in settings.database_url else {}
            )
            
            # Create session maker
            self.async_session = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=True,
                autocommit=False
            )
            
            logger.info("Database service initialized successfully")
            self._initialized = True
            
        except Exception as e:
            logger.error(f"Failed to initialize database service: {e}")
            raise
    
    async def create_tables(self):
        """Create all database tables"""
        
        if not self._initialized:
            await self.initialize()
            
        try:
            async with self.engine.begin() as conn:
                # Import all models to ensure they are registered
                from app.models import (
                    User, Conversation, Message, VectorDocument, DocumentChunk
                )
                
                # Create all tables
                await conn.run_sync(SQLModel.metadata.create_all)
                logger.info("Database tables created successfully")
                
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    async def drop_tables(self):
        """Drop all database tables (use with caution!)"""
        
        if not self._initialized:
            await self.initialize()
            
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.drop_all)
                logger.info("Database tables dropped successfully")
                
        except Exception as e:
            logger.error(f"Failed to drop database tables: {e}")
            raise
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get async database session with automatic cleanup"""
        
        if not self._initialized:
            await self.initialize()
            
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def health_check(self) -> bool:
        """Check database connectivity"""
        
        try:
            async with self.get_session() as session:
                await session.execute("SELECT 1")
                return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    async def close(self):
        """Close database connections"""
        
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connections closed")


# Global database service instance
db_service = DatabaseService()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session"""
    
    async with db_service.get_session() as session:
        yield session


async def init_db():
    """Initialize database - create tables if they don't exist"""
    
    await db_service.initialize()
    await db_service.create_tables()


async def close_db():
    """Close database connections"""
    
    await db_service.close()
