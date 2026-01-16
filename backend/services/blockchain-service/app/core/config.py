from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Blockchain Service"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Blockchain
    BLOCKCHAIN_NETWORK: str = "ethereum"  # ethereum, polygon, bsc
    WEB3_PROVIDER_URL: str = "https://mainnet.infura.io/v3/YOUR_KEY"
    CONTRACT_ADDRESS: str = "0x..."
    PRIVATE_KEY: str = "your-private-key"
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@postgres:5432/blockchain_db"
    
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
