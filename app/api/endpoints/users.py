from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID, uuid4
from app.db.session import get_db
from app.models.user import User as UserModel
from app import models  # Add this import
from app.schemas.user import UserCreate, UserResponse  # Add UserResponse import
import logging
import json
router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating new user with alias: {user.alias}")
    db_user = UserModel(
        alias=user.alias,
        is_ai=user.is_ai,
        config=json.dumps(user.config),
        sessions=[],
        id=str(uuid4())
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.config = json.loads(db_user.config) if db_user.config else None
    return db_user

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    logger.info(f"Fetching user with id: {user_id}")
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.config = json.loads(user.config) if user.config else None
    return user

