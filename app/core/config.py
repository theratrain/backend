from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "TheraTrain Platform API"
    DATABASE_URL: str = "sqlite:///./training.db"
    LOG_LEVEL: str = "INFO"
    GROQ_API_KEY: str = ""
    DEFAULT_MODEL: str = "llama-3.2-90b-vision-preview"
    
    class Config:
        env_file = ".env"

settings = Settings() 