"""
Database configuration and connection management
Using SQLModel for modern async ORM with Pydantic integration
"""

from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel, Session, create_engine
from loguru import logger

from app.core.config import settings


# Async engine for production use
async_engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.DEBUG,
    future=True,
)

# Session factory for async operations
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# Sync engine for migrations and testing
sync_engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)


async def init_db() -> None:
    """Initialize database tables"""
    try:
        async with async_engine.begin() as conn:
            # Import all models here to ensure they're registered
            from app.models.user import User
            from app.models.conversation import Conversation, Message
            from app.models.vector_store import VectorDocument
            
            # Create all tables
            await conn.run_sync(SQLModel.metadata.create_all)
            
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        raise


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()


def get_sync_session() -> Session:
    """Get synchronous database session for migrations"""
    return Session(sync_engine)


async def close_db_connections():
    """Close all database connections"""
    await async_engine.dispose()
    sync_engine.dispose()
    logger.info("📁 Database connections closed")
