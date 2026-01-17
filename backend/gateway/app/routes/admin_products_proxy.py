import os
import httpx
from fastapi import APIRouter, Request, Response

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_URL", "http://product-service:8002")

def _copy_headers(request: Request) -> dict:
    headers = {}
    auth = request.headers.get("authorization")
    if auth:
        headers["authorization"] = auth
    return headers

@router.get("/products")
async def proxy_list_products(request: Request):
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.get(
            f"{PRODUCT_SERVICE_URL}/api/v1/admin/products",
            params=request.query_params,
            headers=_copy_headers(request),
        )
    return Response(
        content=r.content,
        status_code=r.status_code,
        media_type=r.headers.get("content-type", "application/json"),
    )

@router.delete("/products/{product_id}")
async def proxy_delete_product(product_id: str, request: Request):
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.delete(
            f"{PRODUCT_SERVICE_URL}/api/v1/admin/products/{product_id}",
            headers=_copy_headers(request),
        )
    return Response(
        content=r.content,
        status_code=r.status_code,
        media_type=r.headers.get("content-type", "application/json"),
    )
