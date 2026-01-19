from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.routes.auth_proxy import router as auth_proxy_router
from app.routes.admin_users_proxy import router as admin_users_proxy_router
from app.routes.admin_products_proxy import router as admin_products_proxy_router
from app.routes.paypal_proxy import router as paypal_proxy_router
from app.routes.config import router as config_router
from app.routes.proxy import router

from app.middleware.cors import add_cors
from app.middleware.waf import SimpleWAFMiddleware
from app.middleware.request_id import RequestIDMiddleware

app = FastAPI(title="API Gateway", version="1.0.0")

# Middlewares
add_cors(app)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SimpleWAFMiddleware)

# Routers
app.include_router(config_router)
app.include_router(auth_proxy_router)
app.include_router(admin_users_proxy_router)
app.include_router(admin_products_proxy_router)
app.include_router(paypal_proxy_router)
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "gateway"}


Instrumentator().instrument(app).expose(app, endpoint="/metrics")
