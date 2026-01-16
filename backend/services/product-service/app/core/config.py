from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URL: str = "mongodb://mongo:27017"
    MONGO_DB: str = "catalog_db"
    REDIS_URL: str = "redis://redis:6379/0"
    SERVICE_NAME: str = "product-service"
    class Config:
        env_file = ".env"

settings = Settings()
