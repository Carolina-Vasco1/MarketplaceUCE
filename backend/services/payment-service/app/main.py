from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.messaging.kafka import init_bus, get_bus
from app.routes.paypal import router as paypal_router
from app.routes.webhooks import router as webhooks_router

app = FastAPI(title="Payment Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    init_bus(settings.KAFKA_BOOTSTRAP)
    await get_bus().start()


@app.on_event("shutdown")
async def on_shutdown():
    try:
        await get_bus().stop()
    except Exception:
        pass


app.include_router(paypal_router)
app.include_router(webhooks_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.SERVICE_NAME}
