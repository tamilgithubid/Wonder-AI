"""
Message model for WonderAI application
Handles chat messages with different types and content
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import JSON
from enum import Enum


class MessageRole(str, Enum):
    """Message role enumeration"""
    
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageType(str, Enum):
    """Message type enumeration"""
    
    TEXT = "text"
    IMAGE = "image"
    MAP = "map"
    FILE = "file"
    SYSTEM = "system"


class MessageStatus(str, Enum):
    """Message processing status"""
    
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"
    STREAMING = "streaming"


class MessageBase(SQLModel):
    """Base message model with shared fields"""
    
    content: str = Field(max_length=10000)
    role: MessageRole = Field(index=True)
    message_type: MessageType = Field(default=MessageType.TEXT)
    status: MessageStatus = Field(default=MessageStatus.PENDING)
    meta_data: Optional[Dict[str, Any]] = Field(default_factory=dict, sa_column=Column(JSON))
    tokens_used: Optional[int] = Field(default=0)
    processing_time: Optional[float] = Field(default=None)


class Message(MessageBase, table=True):
    """Message table model"""
    
    id: Optional[str] = Field(default=None, primary_key=True, max_length=50)
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    parent_message_id: Optional[str] = Field(default=None)
    
    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    """Schema for creating a new message"""
    
    conversation_id: str


class MessageUpdate(SQLModel):
    """Schema for updating message information"""
    
    content: Optional[str] = Field(default=None, max_length=10000)
    status: Optional[MessageStatus] = Field(default=None)
    metadata: Optional[Dict[str, Any]] = Field(default=None)
    tokens_used: Optional[int] = Field(default=None)
    processing_time: Optional[float] = Field(default=None)


class MessageRead(MessageBase):
    """Schema for reading message data"""
    
    id: str
    conversation_id: str
    created_at: datetime
    updated_at: datetime
    parent_message_id: Optional[str]


class MessageWithContent(MessageRead):
    """Extended message schema with rich content"""
    
    images: List[str] = []
    maps: List[Dict[str, Any]] = []
    files: List[Dict[str, Any]] = []


class StreamingMessage(SQLModel):
    """Schema for streaming message updates"""
    
    id: str
    content_delta: str
    status: MessageStatus
    metadata: Optional[Dict[str, Any]] = None
