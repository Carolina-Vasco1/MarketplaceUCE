from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "local"
    POSTGRES_URL: str = "postgresql+asyncpg://order:order@postgres:5432/order_db"
    KAFKA_BOOTSTRAP: str = "kafka:9092"
    SERVICE_NAME: str = "order-service"

    class Config:
        env_file = ".env"

settings = Settings()
