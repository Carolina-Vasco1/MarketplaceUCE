from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.routes import reviews
from app.deps.db import get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Review Service starting...")
    yield
    print("Review Service shutting down...")

app = FastAPI(
    title="Review Service",
    description="Microservicio de gestión de reseñas y calificaciones",
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

app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["reviews"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "review-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
