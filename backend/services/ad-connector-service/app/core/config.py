from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ad Connector Service"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Google Ads
    GOOGLE_ADS_CUSTOMER_ID: str = ""
    GOOGLE_ADS_API_KEY: str = ""
    GOOGLE_ADS_DEVELOPER_TOKEN: str = ""
    
    # Facebook Ads
    FACEBOOK_ADS_ACCOUNT_ID: str = ""
    FACEBOOK_ADS_ACCESS_TOKEN: str = ""
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@postgres:5432/ads_db"
    
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
