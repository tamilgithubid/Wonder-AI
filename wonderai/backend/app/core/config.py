"""
Core configuration management using Pydantic Settings
Handles environment variables and application settings
"""

import os
from typing import List, Optional, Union
from pydantic import Field, validator
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    APP_NAME: str = "WonderAI"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    # Server
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # Security
    SECRET_KEY: str = Field(env="SECRET_KEY", default="your-secret-key-here-change-in-production")
    ALLOWED_HOSTS: List[str] = Field(default=["*"], env="ALLOWED_HOSTS")
    CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:5173", 
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173"
        ], 
        env="CORS_ORIGINS"
    )
    
    # Database
    DATABASE_URL: Optional[str] = Field(env="DATABASE_URL")
    DB_HOST: str = Field(default="localhost", env="DB_HOST")
    DB_PORT: int = Field(default=5432, env="DB_PORT") 
    DB_NAME: str = Field(default="wonderai", env="DB_NAME")
    DB_USER: str = Field(default="postgres", env="DB_USER")
    DB_PASSWORD: str = Field(default="postgres", env="DB_PASSWORD")
    
    # Google Gemini Configuration
    GOOGLE_API_KEY: Optional[str] = Field(None, env="GOOGLE_API_KEY")
    GEMINI_MODEL: str = Field(default="gemini-2.0-flash-exp", env="GEMINI_MODEL")
    GEMINI_EMBEDDING_MODEL: str = Field(default="text-embedding-004", env="GEMINI_EMBEDDING_MODEL")
    GEMINI_IMAGE_MODEL: str = Field(default="gemini-2.0-flash-exp", env="GEMINI_IMAGE_MODEL")
    
    # OpenAI Configuration (for fallback)
    OPENAI_API_KEY: Optional[str] = Field(None, env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4", env="OPENAI_MODEL")
    OPENAI_EMBEDDING_MODEL: str = Field(default="text-embedding-ada-002", env="OPENAI_EMBEDDING_MODEL")
    OPENAI_IMAGE_MODEL: str = Field(default="dall-e-3", env="OPENAI_IMAGE_MODEL")
    
    # Vector Database
    VECTOR_STORE_PATH: str = Field(default="./data/vector_store", env="VECTOR_STORE_PATH")
    EMBEDDING_DIMENSION: int = Field(default=1536, env="EMBEDDING_DIMENSION")  # OpenAI ada-002 dimension
    
    # Redis (for caching and pub/sub)
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # File Storage
    UPLOAD_DIR: str = Field(default="./uploads", env="UPLOAD_DIR")
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="structured", env="LOG_FORMAT")  # structured or json
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    
    # WebSocket
    WS_HEARTBEAT_INTERVAL: int = Field(default=30, env="WS_HEARTBEAT_INTERVAL")
    
    @validator("DATABASE_URL", pre=True)
    def build_database_url(cls, v, values):
        """Build database URL from components if not provided"""
        if v:
            return v
        
        return (
            f"postgresql://{values.get('DB_USER')}:{values.get('DB_PASSWORD')}"
            f"@{values.get('DB_HOST')}:{values.get('DB_PORT')}/{values.get('DB_NAME')}"
        )
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("ALLOWED_HOSTS", pre=True)
    def parse_allowed_hosts(cls, v):
        """Parse allowed hosts from string or list"""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    # Lowercase property aliases for backward compatibility
    @property
    def environment(self) -> str:
        return self.ENVIRONMENT
    
    @property
    def debug(self) -> bool:
        return self.DEBUG
        
    @property
    def host(self) -> str:
        return self.HOST
        
    @property
    def port(self) -> int:
        return self.PORT
        
    @property
    def database_url(self) -> str:
        return self.DATABASE_URL
        
    @property
    def openai_api_key(self) -> Optional[str]:
        return self.OPENAI_API_KEY
    
    @property
    def google_api_key(self) -> Optional[str]:
        return self.GOOGLE_API_KEY

    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.ENVIRONMENT.lower() in ["development", "dev", "local"]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.ENVIRONMENT.lower() in ["production", "prod"]
    
    @property
    def database_dsn(self) -> str:
        """Get database DSN for SQLModel"""
        return self.DATABASE_URL
    
    def ensure_directories(self):
        """Ensure required directories exist"""
        dirs_to_create = [
            Path(self.UPLOAD_DIR),
            Path(self.VECTOR_STORE_PATH).parent,
            Path("./logs"),
            Path("./data"),
        ]
        
        for directory in dirs_to_create:
            directory.mkdir(parents=True, exist_ok=True)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
_settings = None


def get_settings() -> Settings:
    """Get settings instance (singleton pattern)"""
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.ensure_directories()
    return _settings


# Create global settings instance
settings = get_settings()
