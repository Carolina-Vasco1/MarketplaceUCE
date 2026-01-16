from fastapi import FastAPI

from app.routes.auth import router as auth_router

app = FastAPI(title="auth-service", version="1.0.0")

# Rutas auth (OTP, register, login)
app.include_router(auth_router)

@app.get("/health")
async def health():
    return {"ok": True}
