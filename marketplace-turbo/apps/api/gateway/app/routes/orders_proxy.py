from fastapi import APIRouter, Request, Response
import httpx

from ..core.config import settings


router = APIRouter(tags=["orders-proxy"])

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

        resp_headers = dict(r.headers)
        resp_headers.pop("transfer-encoding", None)
        resp_headers.pop("connection", None)

        return Response(
            content=r.content,
            status_code=r.status_code,
            headers=resp_headers,
        )

@router.api_route("/api/v1/orders", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
@router.api_route("/api/v1/orders/", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def orders_root(request: Request):
    return await _forward(request, settings.ORDER_URL)

@router.api_route("/api/v1/orders/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def orders_subpath(request: Request, path: str):
    return await _forward(request, settings.ORDER_URL)
