"""
User model for WonderAI application
Represents users and their sessions in the system
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import JSON
from pydantic import EmailStr


class UserBase(SQLModel):
    """Base user model with shared fields"""
    
    username: str = Field(index=True, max_length=50)
    email: Optional[EmailStr] = Field(default=None, index=True)
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    preferences: Optional[dict] = Field(default_factory=dict, sa_column=Column(JSON))


class User(UserBase, table=True):
    """User table model"""
    
    id: Optional[str] = Field(default=None, primary_key=True, max_length=50)
    hashed_password: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_seen: Optional[datetime] = Field(default=None)
    
    # Relationships
    conversations: List["Conversation"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """Schema for creating a new user"""
    
    password: Optional[str] = Field(default=None, min_length=8)


class UserUpdate(SQLModel):
    """Schema for updating user information"""
    
    username: Optional[str] = Field(default=None, max_length=50)
    email: Optional[EmailStr] = Field(default=None)
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: Optional[bool] = Field(default=None)
    preferences: Optional[dict] = Field(default=None)


class UserRead(UserBase):
    """Schema for reading user data (public fields)"""
    
    id: str
    created_at: datetime
    last_seen: Optional[datetime]


class UserSession(SQLModel):
    """User session information for temporary users"""
    
    user_id: str
    session_token: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = Field(default=None)
    ip_address: Optional[str] = Field(default=None)
    user_agent: Optional[str] = Field(default=None)
