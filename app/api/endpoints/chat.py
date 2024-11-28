from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict
from app.db.session import get_db
from app.services.chat_service import ChatService
from app.models.session import Session
from app.models.user import User
import logging
import uuid

router = APIRouter()
logger = logging.getLogger(__name__)
chat_service = ChatService()

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    session_id: str

@router.post("/{session_id}", response_model=ChatResponse)
async def chat(
    session_id: str,
    message: ChatMessage,
    db: Session = Depends(get_db)
):
    """
    Send a message in a chat session and get a response
    """
    logger.info(f"Processing chat message for session {session_id}")
    # Get session
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        logger.warning(f"Attempted to chat with non-existent session: {session_id}")
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        chat_service = ChatService(db=db)
        # Get response from LLM
        response = chat_service.get_chat_response(session, message.message)
        
        # Save updated transcript
        db.commit()
        logger.success(f"Chat message processed for session {session_id}")
        
        return ChatResponse(
            response=response,
            session_id=session_id
        )
    except Exception as e:
        logger.error(f"Chat processing failed for session {session_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error processing chat message")

@router.post("/new/{user_id}", response_model=ChatResponse)
async def start_new_chat(
    user_id: str,
    message: ChatMessage,
    db: Session = Depends(get_db)
):
    """
    Start a new chat session and send first message
    """
    
    logger.info(f"Starting new chat for user {user_id}")
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"Attempted to start chat for non-existent user: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        chat_service = ChatService(db=db)
        # Create new session with initial transcript
        session = Session(
            id=str(uuid.uuid4()),
            user_id=user_id,
            transcript=f"THERAPEUT*IN: {message.message}"  # Initialize transcript with first message
        )
        db.add(session)
        db.commit()
        
        # Get response from LLM
        response = chat_service.get_chat_response(session, message.message)
        
        return ChatResponse(
            response=response,
            session_id=session.id
        )
        
    except Exception as e:
        logger.error(f"Failed to start new chat for user {user_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error starting new chat") 