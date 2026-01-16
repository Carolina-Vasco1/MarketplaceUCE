import os
from fastapi import APIRouter, Request, Response
import httpx

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

# ✅ usa AUTH_URL que YA existe en docker-compose
AUTH_SERVICE_URL = os.getenv("AUTH_URL", "http://auth-service:8001")

def _auth_headers(request: Request) -> dict:
    headers = {}
    if "authorization" in request.headers:
        headers["authorization"] = request.headers["authorization"]
    return headers

@router.get("/users")
async def proxy_list_users(request: Request):
    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.get(
            f"{AUTH_SERVICE_URL}/api/v1/admin/users",
            headers=_auth_headers(request),
        )
    return Response(
        content=r.content,
        status_code=r.status_code,
        media_type=r.headers.get("content-type", "application/json"),
    )

@router.patch("/users/{user_id}/role")
async def proxy_set_role(user_id: str, request: Request):
    payload = await request.json()
    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.patch(
            f"{AUTH_SERVICE_URL}/api/v1/admin/users/{user_id}/role",
            headers=_auth_headers(request),
            json=payload,
        )
    return Response(
        content=r.content,
        status_code=r.status_code,
        media_type=r.headers.get("content-type", "application/json"),
    )

@router.patch("/users/{user_id}/active")
async def proxy_set_active(user_id: str, request: Request):
    payload = await request.json()
    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.patch(
            f"{AUTH_SERVICE_URL}/api/v1/admin/users/{user_id}/active",
            headers=_auth_headers(request),
            json=payload,
        )
    return Response(
        content=r.content,
        status_code=r.status_code,
        media_type=r.headers.get("content-type", "application/json"),
    )
