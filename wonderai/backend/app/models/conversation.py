"""
Conversation model for WonderAI application
Manages chat conversations and their metadata
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import JSON
from enum import Enum


class ConversationStatus(str, Enum):
    """Conversation status enumeration"""
    
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class ConversationBase(SQLModel):
    """Base conversation model with shared fields"""
    
    title: str = Field(max_length=200, default="New Conversation")
    status: ConversationStatus = Field(default=ConversationStatus.ACTIVE)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, sa_column=Column(JSON))
    settings: Optional[Dict[str, Any]] = Field(default_factory=dict, sa_column=Column(JSON))


class Conversation(ConversationBase, table=True):
    """Conversation table model"""
    
    id: Optional[str] = Field(default=None, primary_key=True, max_length=50)
    user_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_message_at: Optional[datetime] = Field(default=None)
    message_count: int = Field(default=0)
    
    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        cascade_delete=True
    )


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation"""
    
    pass


class ConversationUpdate(SQLModel):
    """Schema for updating conversation information"""
    
    title: Optional[str] = Field(default=None, max_length=200)
    status: Optional[ConversationStatus] = Field(default=None)
    context: Optional[Dict[str, Any]] = Field(default=None)
    settings: Optional[Dict[str, Any]] = Field(default=None)


class ConversationRead(ConversationBase):
    """Schema for reading conversation data"""
    
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    last_message_at: Optional[datetime]
    message_count: int


class ConversationWithMessages(ConversationRead):
    """Schema for reading conversation with its messages"""
    
    messages: List["MessageRead"] = []
