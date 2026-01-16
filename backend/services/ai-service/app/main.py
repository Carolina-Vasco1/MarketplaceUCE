from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.routes import recommendations, nlp, image_analysis

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("AI Service starting...")
    yield
    print("AI Service shutting down...")

app = FastAPI(
    title="AI Service",
    description="Microservicio de IA - Recomendaciones, NLP, Análisis de imágenes",
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

app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["recommendations"])
app.include_router(nlp.router, prefix="/api/v1/nlp", tags=["nlp"])
app.include_router(image_analysis.router, prefix="/api/v1/images", tags=["image-analysis"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "ai-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)
