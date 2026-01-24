import os
from fastapi import Depends, HTTPException, Request
import jwt

JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret_change_me")
JWT_ALG = os.getenv("JWT_ALG", "HS256")

def _get_token_from_header(request: Request) -> str:
    auth = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    return auth.split(" ", 1)[1].strip()

def require_admin(request: Request = None):
    if request is None:
        # FastAPI inyecta Request si lo pones como dependencia
        raise HTTPException(status_code=500, detail="Request not provided")

    token = _get_token_from_header(request)
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    role = payload.get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    return payload
