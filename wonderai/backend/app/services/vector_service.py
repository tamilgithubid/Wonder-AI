"""
Vector store service for RAG functionality
Handles document indexing, similarity search, and context retrieval
"""

import json
import uuid
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

try:
    import faiss
    import numpy as np
except ImportError:
    # Fallback for development
    faiss = None
    np = None

from app.core.config import get_settings
from app.core.logging import get_logger
from app.services.openai_service import openai_service

logger = get_logger(__name__)
settings = get_settings()


class VectorStoreService:
    """Service for managing vector embeddings and similarity search"""
    
    def __init__(self):
        self.index = None
        self.documents = {}  # document_id -> metadata
        self.chunks = {}     # chunk_id -> content and metadata
        self.dimension = 1536  # text-embedding-3-small dimension
        self._initialized = False
    
    async def initialize(self):
        """Initialize FAISS vector store"""
        
        if self._initialized:
            return
            
        if not faiss or not np:
            raise ImportError("FAISS or NumPy not installed")
        
        try:
            # Create FAISS index (using IndexFlatIP for cosine similarity)
            self.index = faiss.IndexFlatIP(self.dimension)
            
            # Load existing index if available
            await self._load_index()
            
            self._initialized = True
            logger.info("Vector store service initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            raise
    
    async def add_documents(
        self,
        documents: List[Dict[str, Any]],
        user_id: Optional[str] = None
    ) -> List[str]:
        """Add documents to vector store with chunking and embedding"""
        
        if not self._initialized:
            await self.initialize()
        
        document_ids = []
        
        for doc in documents:
            try:
                # Generate document ID
                doc_id = str(uuid.uuid4())
                document_ids.append(doc_id)
                
                # Store document metadata
                self.documents[doc_id] = {
                    "id": doc_id,
                    "title": doc.get("title", "Untitled"),
                    "doc_type": doc.get("doc_type", "text"),
                    "user_id": user_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "metadata": doc.get("metadata", {})
                }
                
                # Chunk document content
                chunks = self._chunk_text(
                    doc.get("content", ""),
                    chunk_size=doc.get("chunk_size", 1000),
                    overlap=doc.get("overlap_size", 200)
                )
                
                # Generate embeddings for chunks
                if chunks:
                    embeddings = await openai_service.generate_embeddings(chunks)
                    
                    # Add chunks to index
                    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                        chunk_id = f"{doc_id}_{i}"
                        
                        # Store chunk data
                        self.chunks[chunk_id] = {
                            "id": chunk_id,
                            "document_id": doc_id,
                            "chunk_index": i,
                            "content": chunk,
                            "metadata": doc.get("metadata", {})
                        }
                        
                        # Add to FAISS index
                        self.index.add(np.array([embedding], dtype=np.float32))
                
                logger.info(f"Added document {doc_id} with {len(chunks)} chunks")
                
            except Exception as e:
                logger.error(f"Error adding document: {e}")
                continue
        
        # Save index after adding documents
        await self._save_index()
        return document_ids
    
    async def search_similar(
        self,
        query: str,
        k: int = 5,
        similarity_threshold: float = 0.7,
        user_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents using vector similarity"""
        
        if not self._initialized:
            await self.initialize()
        
        try:
            # Generate query embedding
            query_embeddings = await openai_service.generate_embeddings([query])
            query_vector = np.array(query_embeddings, dtype=np.float32)
            
            # Search in FAISS index
            scores, indices = self.index.search(query_vector, k)
            
            results = []
            chunk_ids = list(self.chunks.keys())
            
            for score, idx in zip(scores[0], indices[0]):
                if idx >= len(chunk_ids) or score < similarity_threshold:
                    continue
                
                chunk_id = chunk_ids[idx]
                chunk = self.chunks[chunk_id]
                doc_id = chunk["document_id"]
                
                # Filter by user if specified
                if user_id and self.documents[doc_id].get("user_id") != user_id:
                    continue
                
                document = self.documents[doc_id]
                
                results.append({
                    "document_id": doc_id,
                    "chunk_id": chunk_id,
                    "content": chunk["content"],
                    "similarity_score": float(score),
                    "metadata": {
                        **chunk["metadata"],
                        "title": document["title"],
                        "doc_type": document["doc_type"],
                        "chunk_index": chunk["chunk_index"]
                    }
                })
            
            # Sort by similarity score (descending)
            results.sort(key=lambda x: x["similarity_score"], reverse=True)
            
            logger.info(f"Found {len(results)} similar chunks for query")
            return results
            
        except Exception as e:
            logger.error(f"Vector search error: {e}")
            return []
    
    async def get_rag_context(
        self,
        query: str,
        max_chunks: int = 5,
        similarity_threshold: float = 0.7,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get RAG context for a query"""
        
        results = await self.search_similar(
            query=query,
            k=max_chunks * 2,  # Get more results to filter
            similarity_threshold=similarity_threshold,
            user_id=user_id
        )
        
        # Limit to max_chunks
        results = results[:max_chunks]
        
        return {
            "query": query,
            "results": results,
            "total_chunks": len(results),
            "max_chunks": max_chunks,
            "similarity_threshold": similarity_threshold
        }
    
    async def delete_document(self, document_id: str) -> bool:
        """Delete a document and its chunks from the vector store"""
        
        try:
            if document_id not in self.documents:
                return False
            
            # Find and remove chunks
            chunks_to_remove = [
                chunk_id for chunk_id, chunk in self.chunks.items()
                if chunk["document_id"] == document_id
            ]
            
            for chunk_id in chunks_to_remove:
                del self.chunks[chunk_id]
            
            # Remove document
            del self.documents[document_id]
            
            # Rebuild index (FAISS doesn't support efficient deletion)
            await self._rebuild_index()
            
            logger.info(f"Deleted document {document_id} and {len(chunks_to_remove)} chunks")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False
    
    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at word boundaries
            if end < len(text):
                # Find last space before the end
                last_space = text.rfind(' ', start, end)
                if last_space > start:
                    end = last_space
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - overlap if end < len(text) else end
            
            if start >= len(text):
                break
        
        return chunks
    
    async def _rebuild_index(self):
        """Rebuild FAISS index from existing chunks"""
        
        if not self.chunks:
            self.index = faiss.IndexFlatIP(self.dimension)
            return
        
        # Get all chunk contents
        contents = [chunk["content"] for chunk in self.chunks.values()]
        
        if contents:
            # Generate embeddings
            embeddings = await openai_service.generate_embeddings(contents)
            
            # Create new index
            self.index = faiss.IndexFlatIP(self.dimension)
            self.index.add(np.array(embeddings, dtype=np.float32))
        
        await self._save_index()
    
    async def _save_index(self):
        """Save FAISS index and metadata to disk"""
        
        try:
            # Save FAISS index
            faiss.write_index(self.index, "/tmp/wonderai_faiss.index")
            
            # Save metadata
            metadata = {
                "documents": self.documents,
                "chunks": self.chunks,
                "dimension": self.dimension
            }
            
            with open("/tmp/wonderai_metadata.json", "w") as f:
                json.dump(metadata, f, indent=2)
            
            logger.debug("Vector store saved to disk")
            
        except Exception as e:
            logger.error(f"Error saving vector store: {e}")
    
    async def _load_index(self):
        """Load FAISS index and metadata from disk"""
        
        try:
            # Load FAISS index
            import os
            if os.path.exists("/tmp/wonderai_faiss.index"):
                self.index = faiss.read_index("/tmp/wonderai_faiss.index")
            
            # Load metadata
            if os.path.exists("/tmp/wonderai_metadata.json"):
                with open("/tmp/wonderai_metadata.json", "r") as f:
                    metadata = json.load(f)
                
                self.documents = metadata.get("documents", {})
                self.chunks = metadata.get("chunks", {})
                self.dimension = metadata.get("dimension", 1536)
            
            logger.info("Vector store loaded from disk")
            
        except Exception as e:
            logger.debug(f"Could not load existing vector store: {e}")
    
    async def health_check(self) -> bool:
        """Check vector store health"""
        
        try:
            if not self._initialized:
                await self.initialize()
            
            # Simple test
            return self.index is not None
            
        except Exception as e:
            logger.error(f"Vector store health check failed: {e}")
            return False


# Global vector store service instance
vector_service = VectorStoreService()
