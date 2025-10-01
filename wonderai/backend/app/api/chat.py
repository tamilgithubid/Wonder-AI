"""
Chat API routes for WonderAI
Handles conversation and message endpoints with streaming support
"""

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_

from app.core.exceptions import ValidationException, ResourceNotFoundException
from app.models import (
    User, Conversation, Message, ConversationCreate, ConversationRead,
    MessageCreate, MessageRead, MessageRole, MessageType, MessageStatus
)
from app.services import get_db_session, openai_service, vector_service, db_service
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/conversations", response_model=ConversationRead)
async def create_conversation(
    conversation_data: ConversationCreate,
    user_id: str,
    db: AsyncSession = Depends(get_db_session)
) -> ConversationRead:
    """Create a new conversation"""
    
    try:
        # Create conversation
        conversation = Conversation(
            id=str(uuid.uuid4()),
            user_id=user_id,
            **conversation_data.model_dump()
        )
        
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        
        logger.info(f"Created conversation {conversation.id} for user {user_id}")
        return ConversationRead.model_validate(conversation)
        
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create conversation")


@router.get("/conversations", response_model=List[ConversationRead])
async def get_conversations(
    user_id: str,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db_session)
) -> List[ConversationRead]:
    """Get user's conversations"""
    
    try:
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        
        result = await db.execute(statement)
        conversations = result.scalars().all()
        
        return [ConversationRead.model_validate(conv) for conv in conversations]
        
    except Exception as e:
        logger.error(f"Error getting conversations: {e}")
        raise HTTPException(status_code=500, detail="Failed to get conversations")


@router.get("/conversations/{conversation_id}", response_model=ConversationRead)
async def get_conversation(
    conversation_id: str,
    user_id: str,
    db: AsyncSession = Depends(get_db_session)
) -> ConversationRead:
    """Get specific conversation"""
    
    try:
        statement = select(Conversation).where(
            and_(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
        )
        
        result = await db.execute(statement)
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise ResourceNotFoundException(f"Conversation {conversation_id} not found")
        
        return ConversationRead.model_validate(conversation)
        
    except ResourceNotFoundException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation: {e}")
        raise HTTPException(status_code=500, detail="Failed to get conversation")


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageRead])
async def get_messages(
    conversation_id: str,
    user_id: str,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db_session)
) -> List[MessageRead]:
    """Get conversation messages"""
    
    try:
        # Verify conversation ownership
        conv_statement = select(Conversation).where(
            and_(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
        )
        conv_result = await db.execute(conv_statement)
        if not conv_result.scalar_one_or_none():
            raise ResourceNotFoundException(f"Conversation {conversation_id} not found")
        
        # Get messages
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .offset(offset)
            .limit(limit)
        )
        
        result = await db.execute(statement)
        messages = result.scalars().all()
        
        return [MessageRead.model_validate(msg) for msg in messages]
        
    except ResourceNotFoundException:
        raise
    except Exception as e:
        logger.error(f"Error getting messages: {e}")
        raise HTTPException(status_code=500, detail="Failed to get messages")


@router.post("/conversations/{conversation_id}/messages", response_model=MessageRead)
async def send_message(
    conversation_id: str,
    message_data: MessageCreate,
    user_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db_session)
) -> MessageRead:
    """Send a message to conversation"""
    
    try:
        # Verify conversation ownership
        conv_statement = select(Conversation).where(
            and_(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
        )
        conv_result = await db.execute(conv_statement)
        conversation = conv_result.scalar_one_or_none()
        if not conversation:
            raise ResourceNotFoundException(f"Conversation {conversation_id} not found")
        
        # Create user message
        user_message = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            content=message_data.content,
            role=MessageRole.USER,
            message_type=message_data.message_type,
            status=MessageStatus.COMPLETED
        )
        
        db.add(user_message)
        
        # Update conversation
        conversation.updated_at = datetime.utcnow()
        conversation.last_message_at = datetime.utcnow()
        conversation.message_count += 1
        
        await db.commit()
        await db.refresh(user_message)
        
        # Generate AI response in background
        background_tasks.add_task(
            generate_ai_response,
            conversation_id,
            user_message.content,
            user_id
        )
        
        logger.info(f"Message sent to conversation {conversation_id}")
        return MessageRead.model_validate(user_message)
        
    except ResourceNotFoundException:
        raise
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to send message")


@router.post("/conversations/{conversation_id}/stream")
async def send_message_stream(
    conversation_id: str,
    message_data: MessageCreate,
    user_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """Send message with streaming response"""
    
    try:
        # Verify conversation ownership
        conv_statement = select(Conversation).where(
            and_(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
        )
        conv_result = await db.execute(conv_statement)
        conversation = conv_result.scalar_one_or_none()
        if not conversation:
            raise ResourceNotFoundException(f"Conversation {conversation_id} not found")
        
        # Create user message
        user_message = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            content=message_data.content,
            role=MessageRole.USER,
            message_type=message_data.message_type,
            status=MessageStatus.COMPLETED
        )
        
        db.add(user_message)
        await db.commit()
        
        # Stream AI response
        return StreamingResponse(
            generate_streaming_response(conversation_id, message_data.content, user_id),
            media_type="text/plain"
        )
        
    except ResourceNotFoundException:
        raise
    except Exception as e:
        logger.error(f"Error in streaming message: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to stream message")


async def generate_ai_response(
    conversation_id: str,
    user_content: str,
    user_id: str
):
    """Generate AI response for a message"""
    
    try:
        async with db_service.get_session() as db:
            # Get conversation history
            statement = (
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.desc())
                .limit(10)
            )
            
            result = await db.execute(statement)
            messages = result.scalars().all()
            
            # Prepare messages for OpenAI
            openai_messages = []
            for msg in reversed(messages):
                openai_messages.append({
                    "role": msg.role.value,
                    "content": msg.content
                })
            
            # Get RAG context
            rag_context = await vector_service.get_rag_context(
                query=user_content,
                user_id=user_id
            )
            
            # Add system message with context
            if rag_context["results"]:
                context_text = "\n\n".join([
                    f"Document: {result['metadata']['title']}\nContent: {result['content']}"
                    for result in rag_context["results"]
                ])
                
                system_message = {
                    "role": "system",
                    "content": f"You are WonderAI, a helpful assistant. Use the following context to answer questions:\n\n{context_text}"
                }
                openai_messages.insert(0, system_message)
            
            # Generate AI response
            response = await openai_service.generate_chat_completion(
                messages=openai_messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Create assistant message
            ai_message = Message(
                id=str(uuid.uuid4()),
                conversation_id=conversation_id,
                content=response["content"],
                role=MessageRole.ASSISTANT,
                message_type=MessageType.TEXT,
                status=MessageStatus.COMPLETED,
                tokens_used=response.get("tokens_used", 0),
                processing_time=response.get("processing_time", 0.0)
            )
            
            db.add(ai_message)
            await db.commit()
            
            logger.info(f"Generated AI response for conversation {conversation_id}")
            
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")


async def generate_streaming_response(conversation_id: str, user_content: str, user_id: str):
    """Generate streaming AI response"""
    
    try:
        async with db_service.get_session() as db:
            # Get conversation history (similar to above)
            statement = (
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.desc())
                .limit(10)
            )
            
            result = await db.execute(statement)
            messages = result.scalars().all()
            
            # Prepare messages
            openai_messages = []
            for msg in reversed(messages):
                openai_messages.append({
                    "role": msg.role.value,
                    "content": msg.content
                })
            
            # Get RAG context
            rag_context = await vector_service.get_rag_context(
                query=user_content,
                user_id=user_id
            )
            
            if rag_context["results"]:
                context_text = "\n\n".join([
                    f"Document: {result['metadata']['title']}\nContent: {result['content']}"
                    for result in rag_context["results"]
                ])
                
                system_message = {
                    "role": "system",
                    "content": f"You are WonderAI, a helpful assistant. Use the following context to answer questions:\n\n{context_text}"
                }
                openai_messages.insert(0, system_message)
            
            # Stream response
            full_content = ""
            ai_message_id = str(uuid.uuid4())
            
            async for chunk in openai_service.generate_streaming_completion(
                messages=openai_messages,
                temperature=0.7,
                max_tokens=1000
            ):
                if chunk.get("content"):
                    full_content += chunk["content"]
                    yield f"data: {chunk['content']}\n\n"
                
                if chunk.get("finished"):
                    # Save complete message to database
                    ai_message = Message(
                        id=ai_message_id,
                        conversation_id=conversation_id,
                        content=full_content,
                        role=MessageRole.ASSISTANT,
                        message_type=MessageType.TEXT,
                        status=MessageStatus.COMPLETED
                    )
                    
                    db.add(ai_message)
                    await db.commit()
                    
                    yield "data: [DONE]\n\n"
                    break
                    
    except Exception as e:
        logger.error(f"Error in streaming response: {e}")
        yield f"data: Error: {str(e)}\n\n"
