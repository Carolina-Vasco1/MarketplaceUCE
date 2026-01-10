from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "local"
    SERVICE_NAME: str = "notification-service"
    KAFKA_BOOTSTRAP: str = "kafka:9092"

    class Config:
        env_file = ".env"

settings = Settings()
