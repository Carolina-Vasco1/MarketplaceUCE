from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "local"
    JWT_SECRET: str = "change-me"
    JWT_ALG: str = "HS256"
    FRONTEND_ORIGIN: str = "http://localhost:5173"

    AUTH_URL: str = "http://auth-service:8001"
    PRODUCT_URL: str = "http://product-service:8002"
    ORDER_URL: str = "http://order-service:8003"
    PAYMENT_URL: str = "http://payment-service:8004"
    NOTIF_URL: str = "http://notification-service:8005"

    class Config:
        env_file = ".env"

settings = Settings()
