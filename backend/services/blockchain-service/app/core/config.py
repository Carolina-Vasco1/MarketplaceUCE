from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "blockchain-service"
    ENV: str = "local"

    POSTGRES_URL: str = "postgresql+asyncpg://blockchain:blockchain@postgres:5432/blockchain_db"
    KAFKA_BOOTSTRAP: str = "kafka:29092"

    KAFKA_TOPICS: str = "order.created,order.created_from_cart,payment.processed,payment.webhook.received,product.created,product.deleted,product.status_updated"

    class Config:
        env_file = ".env"

settings = Settings()
