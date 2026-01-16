from fastapi import APIRouter, Request, Response
import httpx

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

AUTH_SERVICE_URL = "http://auth-service:8000"  # nombre del service en docker-compose

@router.get("/users")
async def proxy_list_users(request: Request):
    headers = {}
    if "authorization" in request.headers:
        headers["authorization"] = request.headers["authorization"]

    async with httpx.AsyncClient() as client:
        r = await client.get(f"{AUTH_SERVICE_URL}/api/v1/admin/users", headers=headers)

    return Response(
        content=r.content,
        status_code=r.status_code,
        media_type=r.headers.get("content-type", "application/json"),
    )
