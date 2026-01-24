import asyncio
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .routes.orders import router as orders_router, compat as orders_compat_router, bus
from .db.session import init_db

app = FastAPI(title="Order Service", version="1.0.0")

app.include_router(orders_router)
app.include_router(orders_compat_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}

@app.on_event("startup")
async def startup():
    await init_db()

    max_tries = 20
    delay = 2

    for _ in range(max_tries):
        try:
            await bus.start()
            break
        except Exception:
            await asyncio.sleep(delay)

@app.on_event("shutdown")
async def shutdown():
    try:
        await bus.stop()
    except Exception:
        pass

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
