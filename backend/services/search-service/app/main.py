from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.routes import search

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Search Service starting...")
    yield
    print("Search Service shutting down...")

app = FastAPI(
    title="Search Service",
    description="Microservicio de búsqueda con MongoDB Atlas",
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

app.include_router(search.router, prefix="/api/v1/search", tags=["search"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "search-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
