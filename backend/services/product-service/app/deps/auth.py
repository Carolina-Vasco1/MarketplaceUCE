import os
import jwt
from fastapi import Depends, HTTPException, Request

JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALG = os.getenv("JWT_ALG", "HS256")


def require_admin(request: Request):
    auth = request.headers.get("authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = auth.split(" ", 1)[1].strip()

    if not JWT_SECRET:
        raise HTTPException(status_code=500, detail="JWT_SECRET not configured in product-service")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    role = payload.get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    return payload
