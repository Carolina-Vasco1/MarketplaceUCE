from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "local"
    SERVICE_NAME: str = "payment-service"

    KAFKA_BOOTSTRAP: str = "kafka:9092"

    PAYPAL_BASE_URL: str = "https://api-m.sandbox.paypal.com"
    PAYPAL_CLIENT_ID: str = ""
    PAYPAL_CLIENT_SECRET: str = ""
    PAYPAL_WEBHOOK_ID: str = ""  # para verificación de firma en prod

    class Config:
        env_file = ".env"

settings = Settings()
