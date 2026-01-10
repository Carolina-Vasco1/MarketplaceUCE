from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from .routes.auth import router as auth_router

app = FastAPI(title="Auth Service", version="1.1.0 (OTP)")

app.include_router(auth_router)

@app.get("/health")
def health():
    return {"status": "ok"}

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
