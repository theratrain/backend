from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.session import Session as SessionModel
from app.schemas.session import Session, SessionCreate
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/{user_id}", response_model=Session)
def create_session(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Create a new empty session for a user"""
    try:
        session = SessionModel(
            user_id=user_id,
            transcript="[]"
        )
        db.add(session)
        db.commit()
        logger.success(f"Created new session for user {user_id}")
        return session
    except Exception as e:
        logger.error(f"Failed to create session for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating session")

@router.get("/user/{user_id}", response_model=List[Session])
def get_user_sessions(
    user_id: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get all sessions for a user"""
    sessions = db.query(SessionModel)\
        .filter(SessionModel.user_id == user_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return sessions

@router.get("/{session_id}", response_model=Session)
def get_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific session by ID"""
    session = db.query(SessionModel)\
        .filter(SessionModel.id == session_id)\
        .first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found") 

@router.delete("/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        logger.warning(f"Attempted to delete non-existent session: {session_id}")
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        db.delete(session)
        db.commit()
        logger.success(f"Deleted session {session_id}")
        return {"message": "Session deleted"}
    except Exception as e:
        logger.error(f"Failed to delete session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting session") 