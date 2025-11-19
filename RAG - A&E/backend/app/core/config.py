"""
Configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    APP_NAME: str = "AI Triage RAG Agent"
    DEBUG: bool = True
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


