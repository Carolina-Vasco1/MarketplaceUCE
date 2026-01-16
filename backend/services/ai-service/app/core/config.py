from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Service"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # AI Models
    OPENAI_API_KEY: str = "your-openai-api-key"
    HUGGINGFACE_API_KEY: str = "your-huggingface-api-key"
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@postgres:5432/ai_service_db"
    REDIS_URL: str = "redis://redis:6379/0"
    
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
