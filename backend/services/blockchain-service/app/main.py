import asyncio
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.db.session import init_db
from app.routes.ledger import router as ledger_router
from app.consumers.kafka_consumer import BlockchainConsumer

app = FastAPI(title="Blockchain Service")

app.include_router(ledger_router, prefix="/ledger", tags=["Ledger"])


consumer = BlockchainConsumer()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "kafka": consumer.enabled
    }

@app.on_event("startup")
async def startup():
    await init_db()
    print("[BLOCKCHAIN] DB ready ✅")

    try:
        await consumer.start()
        asyncio.create_task(consumer.run_forever())
        print("[BLOCKCHAIN] Kafka running ✅")
    except Exception as e:
        print("[BLOCKCHAIN] Kafka disabled ⚠️", repr(e))

@app.on_event("shutdown")
async def shutdown():
    await consumer.stop()

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
