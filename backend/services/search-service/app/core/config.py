from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Search Service"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # MongoDB Atlas
    MONGODB_URL: str = "mongodb+srv://user:password@cluster.mongodb.net/marketplace?retryWrites=true&w=majority"
    MONGODB_DB: str = "marketplace"
    
    # Elasticsearch (optional)
    ELASTICSEARCH_URL: str = "http://elasticsearch:9200"
    
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
