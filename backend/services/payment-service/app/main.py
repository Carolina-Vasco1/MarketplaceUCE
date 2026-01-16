from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from .routes.webhooks import router, bus

app = FastAPI(title="Payment Service", version="1.0.0")
app.include_router(router)

@app.on_event("startup")
async def _startup():
    await bus.start()

@app.on_event("shutdown")
async def _shutdown():
    await bus.stop()

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
