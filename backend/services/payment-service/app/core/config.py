from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "local"
    SERVICE_NAME: str = "payment-service"

    KAFKA_BOOTSTRAP: str = "kafka:29092"  # OJO: en tu compose kafka interno usa 29092

    PAYPAL_ENV: str = "sandbox"  # ✅ NUEVO
    PAYPAL_BASE_URL: str = "https://api-m.sandbox.paypal.com"
    PAYPAL_CLIENT_ID: str = ""
    PAYPAL_CLIENT_SECRET: str = ""
    PAYPAL_WEBHOOK_ID: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
