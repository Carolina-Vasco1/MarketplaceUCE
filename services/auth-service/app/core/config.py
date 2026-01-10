import os
from pydantic import BaseModel

class Settings(BaseModel):
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "postgresql+asyncpg://auth:auth@postgres:5432/auth_db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")

    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev_secret_change_me")
    JWT_ALG: str = os.getenv("JWT_ALG", "HS256")
    JWT_EXPIRES_MIN: int = int(os.getenv("JWT_EXPIRES_MIN", "1440"))

    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM: str = os.getenv("SMTP_FROM", os.getenv("SMTP_USER", ""))

    OTP_TTL_SECONDS: int = int(os.getenv("OTP_TTL_SECONDS", "300"))          # 5 min
    OTP_RESEND_COOLDOWN: int = int(os.getenv("OTP_RESEND_COOLDOWN", "60"))   # 60s
    OTP_VERIFIED_TTL: int = int(os.getenv("OTP_VERIFIED_TTL", "900"))        # 15 min

settings = Settings()

