from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = "local"
    SERVICE_NAME: str = "payment-service"

    KAFKA_BOOTSTRAP: str = "kafka:29092"

    PAYPAL_ENV: str = "sandbox"
    PAYPAL_BASE_URL: str = "https://api-m.sandbox.paypal.com"
    PAYPAL_CLIENT_ID: str = ""
    PAYPAL_CLIENT_SECRET: str = ""
    PAYPAL_WEBHOOK_ID: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
