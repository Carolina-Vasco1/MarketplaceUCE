from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.routes import categories
from app.deps.db import get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Category Service starting...")
    yield
    # Shutdown
    print("Category Service shutting down...")

app = FastAPI(
    title="Category Service",
    description="Microservicio de gestión de categorías",
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
app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "category-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
