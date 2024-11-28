from pydantic import BaseModel
from uuid import UUID
from .analysis import Analysis

class SessionBase(BaseModel):
    transcript: str

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    id: UUID
    analysis: Analysis

    class Config:
        from_attributes = True 