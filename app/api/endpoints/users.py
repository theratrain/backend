from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db.session import get_db
from app.schemas.user import User, UserCreate
import logging
import json

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating new user with alias: {user.alias}")
    db_user = User(
        alias=user.alias,
        is_ai=user.is_ai,
        config=json.dumps(user.config)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=User)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    logger.info(f"Fetching user with id: {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user 

