import asyncio
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.db.session import init_db
from app.routes.ledger import router as ledger_router
from app.consumers.kafka_consumer import BlockchainConsumer

app = FastAPI(title="Blockchain Service", version="1.0.0")

app.include_router(ledger_router)

consumer = BlockchainConsumer()

@app.get("/health")
def health():
    return {"status": "ok", "service": "blockchain-service"}

@app.on_event("startup")
async def startup():
    await init_db()
    print("[BLOCKCHAIN] DB init ✅")

    max_tries = 30
    delay = 2

    for i in range(1, max_tries + 1):
        try:
            await consumer.start()
            asyncio.create_task(consumer.run_forever())
            print(f"[BLOCKCHAIN] Kafka connected ✅ (try {i})")
            break
        except Exception as e:
            print(f"[BLOCKCHAIN] Kafka not ready (try {i}/{max_tries}): {repr(e)}")
            await asyncio.sleep(delay)

@app.on_event("shutdown")
async def shutdown():
    try:
        await consumer.stop()
    except Exception as e:
        print("[BLOCKCHAIN] stop error:", repr(e))

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
