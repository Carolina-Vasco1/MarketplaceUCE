from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.routes import google_ads, facebook_ads, campaigns

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Ad Connector Service starting...")
    yield
    print("Ad Connector Service shutting down...")

app = FastAPI(
    title="Ad Connector Service",
    description="Microservicio para integración con plataformas de publicidad",
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

app.include_router(google_ads.router, prefix="/api/v1/google-ads", tags=["google-ads"])
app.include_router(facebook_ads.router, prefix="/api/v1/facebook-ads", tags=["facebook-ads"])
app.include_router(campaigns.router, prefix="/api/v1/campaigns", tags=["campaigns"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "ad-connector-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
