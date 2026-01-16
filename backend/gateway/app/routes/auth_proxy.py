import os
from fastapi import APIRouter, Request, Response
import httpx

router = APIRouter(prefix="/auth", tags=["auth"])

# Usa tu variable del docker-compose
AUTH_SERVICE_URL = os.getenv("AUTH_URL", "http://auth-service:8001")

@router.post("/login")
async def proxy_login(request: Request):
    payload = await request.json()
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.post(f"{AUTH_SERVICE_URL}/auth/login", json=payload)

    return Response(
        content=r.content,
        status_code=r.status_code,
        media_type=r.headers.get("content-type", "application/json"),
    )
