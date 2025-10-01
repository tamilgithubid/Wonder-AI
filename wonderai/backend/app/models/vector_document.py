"""
Vector document model for WonderAI RAG functionality
Handles document storage and vector embeddings
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from enum import Enum


class DocumentType(str, Enum):
    """Document type enumeration"""
    
    TEXT = "text"
    PDF = "pdf"
    MARKDOWN = "markdown"
    WEB = "web"
    CONVERSATION = "conversation"
    USER_UPLOAD = "user_upload"


class DocumentStatus(str, Enum):
    """Document processing status"""
    
    PENDING = "pending"
    PROCESSING = "processing"
    INDEXED = "indexed"
    ERROR = "error"
    ARCHIVED = "archived"


class VectorDocumentBase(SQLModel):
    """Base vector document model"""
    
    title: str = Field(max_length=500)
    content: str = Field(max_length=50000)
    doc_type: DocumentType = Field(index=True)
    status: DocumentStatus = Field(default=DocumentStatus.PENDING, index=True)
    source_url: Optional[str] = Field(default=None, max_length=2000)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, sa_column=Column(JSON))
    chunk_size: int = Field(default=1000)
    overlap_size: int = Field(default=200)


class VectorDocument(VectorDocumentBase, table=True):
    """Vector document table model"""
    
    id: Optional[str] = Field(default=None, primary_key=True, max_length=50)
    user_id: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    indexed_at: Optional[datetime] = Field(default=None)
    vector_id: Optional[str] = Field(default=None, index=True)
    embedding_model: str = Field(default="text-embedding-3-small")
    chunk_count: int = Field(default=0)


class VectorDocumentCreate(VectorDocumentBase):
    """Schema for creating a new vector document"""
    
    pass


class VectorDocumentUpdate(SQLModel):
    """Schema for updating vector document"""
    
    title: Optional[str] = Field(default=None, max_length=500)
    content: Optional[str] = Field(default=None, max_length=50000)
    status: Optional[DocumentStatus] = Field(default=None)
    metadata: Optional[Dict[str, Any]] = Field(default=None)


class VectorDocumentRead(VectorDocumentBase):
    """Schema for reading vector document data"""
    
    id: str
    user_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    indexed_at: Optional[datetime]
    vector_id: Optional[str]
    embedding_model: str
    chunk_count: int


class DocumentChunk(SQLModel, table=True):
    """Document chunk for vector storage"""
    
    id: Optional[str] = Field(default=None, primary_key=True, max_length=50)
    document_id: str = Field(foreign_key="vectordocument.id", index=True)
    chunk_index: int = Field(index=True)
    content: str = Field(max_length=10000)
    vector_id: Optional[str] = Field(default=None, index=True)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SearchResult(SQLModel):
    """Search result schema for RAG queries"""
    
    document_id: str
    chunk_id: str
    content: str
    similarity_score: float
    metadata: Dict[str, Any]
    title: str


class RAGContext(SQLModel):
    """RAG context for message generation"""
    
    query: str
    results: List[SearchResult]
    total_chunks: int
    max_chunks: int = 5
    similarity_threshold: float = 0.7
