from fastapi import APIRouter, Request, Response
import httpx

from app.core.config import settings

router = APIRouter(prefix="/order", tags=["orders-proxy"])
METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

@router.api_route("/{path:path}", methods=METHODS)
async def orders_proxy(request: Request, path: str) -> Response:
    upstream = settings.ORDER_URL.rstrip("/")
    new_path = "/" + path.lstrip("/")

    headers = dict(request.headers)
    headers.pop("host", None)

    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.request(
            method=request.method,
            url=f"{upstream}{new_path}",
            params=request.query_params,  # ✅ correcto
            content=await request.body(),
            headers=headers,
        )

    resp_headers = dict(r.headers)
    resp_headers.pop("transfer-encoding", None)
    resp_headers.pop("connection", None)

    return Response(content=r.content, status_code=r.status_code, headers=resp_headers)
