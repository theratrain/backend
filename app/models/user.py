from sqlalchemy import Column, String, Boolean, JSON, Text
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    is_ai = Column(Boolean, default=False)
    alias = Column(String, unique=True, index=True)
    config = Column(Text)
    
    # Relationships
    sessions = relationship("Session", backref="user")