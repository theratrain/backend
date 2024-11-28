from fastapi import FastAPI
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api.endpoints import users, chat, sessions, analysis
from app.db.session import engine, Base
from fastapi.middleware.cors import CORSMiddleware

# Setup logging
setup_logging()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your Vite frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(analysis.router, prefix="/analysis", tags=["analysis"]) 
