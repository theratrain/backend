from fastapi import FastAPI
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api.endpoints import users
from app.db.session import engine, Base

# Setup logging
setup_logging()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"]) 