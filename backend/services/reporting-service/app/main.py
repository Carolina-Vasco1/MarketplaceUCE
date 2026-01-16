from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.routes import reports, sales, analytics

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Reporting Service starting...")
    yield
    print("Reporting Service shutting down...")

app = FastAPI(
    title="Reporting Service",
    description="Microservicio de reportes y análisis",
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

app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])
app.include_router(sales.router, prefix="/api/v1/sales", tags=["sales"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "reporting-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)
