from sqlalchemy import Column, String, Boolean, JSON, Text
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    is_ai = Column(Boolean, default=False)
    alias = Column(String)
    config = Column(String, nullable=True)
    
    # Relationships
    sessions = relationship("Session", backref="user")