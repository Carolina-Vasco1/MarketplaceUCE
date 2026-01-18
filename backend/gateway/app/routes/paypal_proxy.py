import os
import httpx
from fastapi import APIRouter, Request, Response

router = APIRouter(tags=["paypal-proxy"])

PAYMENT_SERVICE_URL = os.getenv("PAYMENT_URL", "http://payment-service:8004")

def _forward_headers(request: Request) -> dict:
    # reenviamos headers útiles (Authorization si lo usas)
    headers = {}
    if "authorization" in request.headers:
        headers["authorization"] = request.headers["authorization"]
    if "content-type" in request.headers:
        headers["content-type"] = request.headers["content-type"]
    return headers

@router.api_route("/api/v1/paypal/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_paypal(path: str, request: Request):
    url = f"{PAYMENT_SERVICE_URL}/api/v1/paypal/{path}"

    body = await request.body()

    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.request(
            method=request.method,
            url=url,
            params=dict(request.query_params),
            content=body,
            headers=_forward_headers(request),
        )

    return Response(
        content=r.content,
        status_code=r.status_code,
        media_type=r.headers.get("content-type", "application/json"),
    )
