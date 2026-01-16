from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.routes.admin_users_proxy import router as admin_users_proxy_router
from .routes.proxy import router
from .middleware.cors import add_cors
from .middleware.waf import SimpleWAFMiddleware
from .middleware.request_id import RequestIDMiddleware

app = FastAPI(title="API Gateway", version="1.0.0")

add_cors(app)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SimpleWAFMiddleware)

app.include_router(admin_users_proxy_router)

app.include_router(router)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
