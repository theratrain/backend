from fastapi import FastAPI
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api.endpoints import users, chat, sessions, analyses
from app.db.session import engine, Base

# Setup logging
setup_logging()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(analyses.router, prefix="/analyses", tags=["analyses"]) 