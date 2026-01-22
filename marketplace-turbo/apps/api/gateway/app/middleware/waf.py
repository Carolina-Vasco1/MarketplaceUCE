from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import re

SUSPICIOUS = [
    re.compile(r"(\.\./|\.\.\\)"),  # path traversal
    re.compile(r"(<script|%3Cscript)", re.IGNORECASE),  # XSS
    re.compile(r"(union\s+select|sleep\(|benchmark\()", re.IGNORECASE),  # SQLi-ish
]

MAX_INSPECT_BYTES = 64 * 1024  # 64KB


class SimpleWAFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        url_text = str(request.url)

        body_bytes = await request.body()

        async def receive():
            return {"type": "http.request", "body": body_bytes, "more_body": False}

        request._receive = receive  # type: ignore

        inspect_bytes = body_bytes[:MAX_INSPECT_BYTES]
        body_text = inspect_bytes.decode("utf-8", errors="ignore")

        raw = f"{url_text} {body_text}"

        for rule in SUSPICIOUS:
            if rule.search(raw):
                return JSONResponse(
                    {"detail": "Blocked by WAF rule"},
                    status_code=403,
                )

        return await call_next(request)
