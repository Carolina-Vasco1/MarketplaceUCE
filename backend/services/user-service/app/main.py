from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.routes import users
from app.deps.db import get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("User Service starting...")
    yield
    # Shutdown
    print("User Service shutting down...")

app = FastAPI(
    title="User Service",
    description="Microservicio de gestión de usuarios",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "user-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
