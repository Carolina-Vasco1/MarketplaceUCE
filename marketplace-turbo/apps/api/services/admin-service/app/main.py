from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.routes import admin, users, reports
from app.deps.db import get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Admin Service starting...")
    yield
    print("Admin Service shutting down...")

app = FastAPI(
    title="Admin Service",
    description="Microservicio de administración",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(users.router, prefix="/api/v1/admin/users", tags=["admin-users"])
app.include_router(reports.router, prefix="/api/v1/admin/reports", tags=["admin-reports"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "admin-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
