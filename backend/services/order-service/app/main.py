import asyncio
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .routes.orders import router as orders_router, bus
from .db.session import init_db

app = FastAPI(title="Order Service", version="1.0.0")
app.include_router(orders_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}

@app.on_event("startup")
async def _startup():
    # ✅ 1) crear tablas
    await init_db()
    print("[ORDER] DB init ✅")

    # ✅ 2) conectar kafka con reintentos (sin tumbar el servicio)
    max_tries = 20
    delay = 2
    connected = False

    for i in range(1, max_tries + 1):
        try:
            await bus.start()
            print(f"[ORDER] Kafka connected ✅ (try {i})")
            connected = True
            break
        except Exception as e:
            print(f"[ORDER] Kafka not ready (try {i}/{max_tries}): {repr(e)}")
            await asyncio.sleep(delay)

    if not connected:
        # 👇 NO hacemos raise. El servicio queda vivo y /health funciona.
        print("[ORDER] Kafka still not available. Service will run without Kafka for now.")

@app.on_event("shutdown")
async def _shutdown():
    try:
        await bus.stop()
    except Exception as e:
        print("[ORDER] Error stopping Kafka:", repr(e))

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
