from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import jwt
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(raw: str) -> str:
    return pwd_context.hash(raw)


def verify_password(raw: str, hashed: str) -> bool:
    return pwd_context.verify(raw, hashed)


def create_access_token(sub: str, role: str, uid: int | None = None) -> str:
    now = datetime.now(timezone.utc)

    payload: Dict[str, Any] = {
        "sub": sub,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.JWT_EXPIRES_MIN)).timestamp()),
        "iss": getattr(settings, "SERVICE_NAME", "auth-service"),
    }

    # opcional: incluir uid si lo mandas
    if uid is not None:
        payload["uid"] = uid

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
