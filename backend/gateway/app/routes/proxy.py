from fastapi import APIRouter, Depends, Request, Response
import httpx

from ..core.security import get_current_user
from ..core.rbac import require_roles
from ..core.config import settings

router = APIRouter()

SERVICE_MAP = {
    "auth": settings.AUTH_URL,
    "products": settings.PRODUCT_URL,
    "order": settings.ORDER_URL,
    "product": settings.PRODUCT_URL,
    "orders": settings.ORDER_URL,
    "payments": settings.PAYMENT_URL,
    "notification": settings.NOTIF_URL,
    "notifications": settings.NOTIF_URL,
    # Additional services (if deployed)
    "user": "http://user-service:8002",
    "category": "http://category-service:8003",
    "review": "http://review-service:8004",
    "search": "http://search-service:8005",
    "admin": "http://admin-service:8006",
    "reporting": "http://reporting-service:8007",
    "ai": "http://ai-service:8008",
}

async def _forward(request: Request, upstream: str) -> Response:
    async with httpx.AsyncClient(timeout=30.0) as client:
        headers = dict(request.headers)
        headers.pop("host", None)

        r = await client.request(
            request.method,
            f"{upstream}{request.url.path}",
            params=request.query_params,
            content=await request.body(),
            headers=headers,
        )

        return Response(
            content=r.content,
            status_code=r.status_code,
            headers=dict(r.headers),
        )


# Auth endpoints (public) - LEGACY
@router.api_route("/auth", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
@router.api_route("/auth/", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def auth_root_proxy(request: Request):
    return await _forward(request, SERVICE_MAP["auth"])

@router.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def auth_proxy(request: Request, path: str):
    return await _forward(request, SERVICE_MAP["auth"])


@router.api_route("/products", methods=["GET"])
@router.api_route("/products/", methods=["GET"])
async def products_public_root(request: Request):
    return await _forward(request, SERVICE_MAP["products"])

@router.api_route("/products/{path:path}", methods=["GET"])
async def products_public_proxy(request: Request, path: str):
    return await _forward(request, SERVICE_MAP["products"])

@router.api_route("/products", methods=["POST", "PUT", "PATCH", "DELETE"])
@router.api_route("/products/", methods=["POST", "PUT", "PATCH", "DELETE"])
async def products_private_root(request: Request, user=Depends(get_current_user)):
    require_roles("seller", "admin")(user)
    return await _forward(request, SERVICE_MAP["products"])

@router.api_route("/products/{path:path}", methods=["POST", "PUT", "PATCH", "DELETE"])
async def products_private_proxy(request: Request, path: str, user=Depends(get_current_user)):
    require_roles("seller", "admin")(user)
    return await _forward(request, SERVICE_MAP["products"])

@router.api_route("/static/{path:path}", methods=["GET"])
async def static_proxy(request: Request, path: str):
    return await _forward(request, SERVICE_MAP["products"])

@router.api_route("/{service}/api/v1", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def service_root_proxy(request: Request, service: str):
    if service not in SERVICE_MAP:
        return Response(status_code=404, content="Service not found")
    return await _forward(request, SERVICE_MAP[service])

@router.api_route("/{service}/api/v1/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def service_proxy(request: Request, service: str, path: str):
    if service not in SERVICE_MAP:
        return Response(status_code=404, content="Service not found")
    return await _forward(request, SERVICE_MAP[service])
