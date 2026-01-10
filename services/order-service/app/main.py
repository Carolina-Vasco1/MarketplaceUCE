from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from .routes.orders import router, bus
from .core.config import settings

app = FastAPI(title="Order Service", version="1.0.0")
app.include_router(router)

@app.on_event("startup")
async def _startup():
    await bus.start()

@app.on_event("shutdown")
async def _shutdown():
    await bus.stop()

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
