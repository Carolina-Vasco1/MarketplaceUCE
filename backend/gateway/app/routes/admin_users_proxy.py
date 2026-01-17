import os
import httpx
from fastapi import APIRouter, Request, Response

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

AUTH_SERVICE_URL = os.getenv("AUTH_URL", "http://auth-service:8001")



def _copy_headers(request: Request) -> dict:
    """
    Copia headers útiles (Authorization).
    """
    headers = {}
    auth = request.headers.get("authorization")
    if auth:
        headers["authorization"] = auth
    return headers


@router.get("/users")
async def proxy_list_users(request: Request):
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.get(
            f"{AUTH_SERVICE_URL}/admin/users",   # ✅ RUTA REAL EN AUTH-SERVICE
            params=request.query_params,
            headers=_copy_headers(request),
        )

    return Response(
        content=r.content,
        status_code=r.status_code,
        media_type=r.headers.get("content-type", "application/json"),
    )

@router.patch("/users/{user_id}/role")
async def proxy_set_role(user_id: str, request: Request):
    payload = await request.json()
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.patch(
            f"{AUTH_SERVICE_URL}/api/v1/admin/users/{user_id}/role",
            headers=_copy_headers(request),
            json=payload,
        )
    return Response(content=r.content, status_code=r.status_code, media_type=r.headers.get("content-type", "application/json"))

@router.patch("/users/{user_id}/active")
async def proxy_set_active(user_id: str, request: Request):
    payload = await request.json()
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.patch(
            f"{AUTH_SERVICE_URL}/api/v1/admin/users/{user_id}/active",
            headers=_copy_headers(request),
            json=payload,
        )
    return Response(content=r.content, status_code=r.status_code, media_type=r.headers.get("content-type", "application/json"))

