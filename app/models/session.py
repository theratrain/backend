from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    transcript = Column(Text)
    user_id = Column(String, ForeignKey('users.id'))
    analysis_id = Column(String, ForeignKey('analyses.id'))
    
    # Relationships
    analysis = relationship("Analysis", backref="session")