from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from .routes.auth import router as auth_router
from app.routes import admin_users
from app.routes.admin_users import router as admin_users_router

app = FastAPI(title="Auth Service", version="1.1.0 (OTP)")

app.include_router(auth_router)

app.include_router(admin_users.router)
app.include_router(admin_users_router)

@app.get("/health")
def health():
    return {"status": "ok"}

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
