from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import re

SUSPICIOUS = [
    re.compile(r"(\.\./|\.\.\\)"),
    re.compile(r"(<script|%3Cscript)", re.IGNORECASE),
    re.compile(r"(union\s+select|sleep\(|benchmark\()", re.IGNORECASE),
]

class SimpleWAFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        raw = str(request.url)
        body = (await request.body()).decode("utf-8", errors="ignore")
        raw = raw + " " + body
        for rule in SUSPICIOUS:
            if rule.search(raw):
                return JSONResponse({"detail": "Blocked by WAF rule"}, status_code=403)
        return await call_next(request)
