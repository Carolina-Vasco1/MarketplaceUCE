import os
from fastapi import APIRouter, Request, Response
import httpx

router = APIRouter(prefix="/auth", tags=["auth"])

AUTH_SERVICE_URL = os.getenv("AUTH_URL", "http://auth-service:8001")

def _copy_headers(request: Request) -> dict:
    headers = dict(request.headers)
    headers.pop("host", None)
    return headers

@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
)
async def proxy_auth(request: Request, path: str):
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.request(
            method=request.method,
            url=f"{AUTH_SERVICE_URL}/auth/{path}",
            params=request.query_params,
            content=await request.body(),
            headers=_copy_headers(request),
        )

    return Response(
        content=r.content,
        status_code=r.status_code,
        media_type=r.headers.get("content-type", "application/json"),
    )
