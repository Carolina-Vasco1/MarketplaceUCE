from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.routes import transactions, contracts, wallet

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Blockchain Service starting...")
    yield
    print("Blockchain Service shutting down...")

app = FastAPI(
    title="Blockchain Service",
    description="Microservicio blockchain - Transacciones, Smart Contracts, Wallets",
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

app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])
app.include_router(contracts.router, prefix="/api/v1/contracts", tags=["contracts"])
app.include_router(wallet.router, prefix="/api/v1/wallet", tags=["wallet"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "blockchain-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)
