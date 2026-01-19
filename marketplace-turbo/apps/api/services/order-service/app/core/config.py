from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = "local"
    POSTGRES_URL: str = "postgresql+asyncpg://order:order@postgres:5432/order_db"
    KAFKA_BOOTSTRAP: str = "kafka:29092"
    SERVICE_NAME: str = "order-service"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
