"""
Models package for WonderAI application
Exports all database models and schemas
"""

from .user import (
    User,
    UserBase,
    UserCreate,
    UserUpdate,
    UserRead,
    UserSession
)

from .conversation import (
    Conversation,
    ConversationBase,
    ConversationCreate,
    ConversationUpdate,
    ConversationRead,
    ConversationWithMessages,
    ConversationStatus
)

from .message import (
    Message,
    MessageBase,
    MessageCreate,
    MessageUpdate,
    MessageRead,
    MessageWithContent,
    StreamingMessage,
    MessageRole,
    MessageType,
    MessageStatus
)

from .vector_document import (
    VectorDocument,
    VectorDocumentBase,
    VectorDocumentCreate,
    VectorDocumentUpdate,
    VectorDocumentRead,
    DocumentChunk,
    SearchResult,
    RAGContext,
    DocumentType,
    DocumentStatus
)

__all__ = [
    # User models
    "User",
    "UserBase", 
    "UserCreate",
    "UserUpdate",
    "UserRead",
    "UserSession",
    
    # Conversation models
    "Conversation",
    "ConversationBase",
    "ConversationCreate",
    "ConversationUpdate", 
    "ConversationRead",
    "ConversationWithMessages",
    "ConversationStatus",
    
    # Message models
    "Message",
    "MessageBase",
    "MessageCreate",
    "MessageUpdate",
    "MessageRead",
    "MessageWithContent",
    "StreamingMessage",
    "MessageRole",
    "MessageType", 
    "MessageStatus",
    
    # Vector document models
    "VectorDocument",
    "VectorDocumentBase",
    "VectorDocumentCreate",
    "VectorDocumentUpdate",
    "VectorDocumentRead", 
    "DocumentChunk",
    "SearchResult",
    "RAGContext",
    "DocumentType",
    "DocumentStatus"
]
