from pydantic import BaseModel
from typing import List, Dict, Optional
from uuid import UUID
from .session import Session

class UserBase(BaseModel):
    alias: str
    is_ai: bool
    config: Dict

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: UUID
    sessions: List[Session]

    class Config:
        from_attributes = True 