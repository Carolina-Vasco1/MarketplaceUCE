import asyncio
import json
import traceback
from aiokafka import AIOKafkaConsumer

from app.core.config import settings
from app.services.ledger_service import LedgerService


class BlockchainConsumer:
    def __init__(self):
        self.enabled = False
        self.consumer = AIOKafkaConsumer(
            "payment.completed",
            bootstrap_servers=settings.KAFKA_BOOTSTRAP,
            group_id="blockchain-service",
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        self.ledger = LedgerService()

    async def start(self):
        # Reintentos para cuando Kafka aún está inicializando (coordinator/topic)
        max_tries = 30
        delay = 2

        for i in range(1, max_tries + 1):
            try:
                await self.consumer.start()
                self.enabled = True
                print(f"[BLOCKCHAIN] Kafka consumer started (try {i})")
                return
            except Exception as e:
                print(f"[BLOCKCHAIN] Kafka not ready ({i}/{max_tries}): {repr(e)}")
                await asyncio.sleep(delay)

        self.enabled = False
        print("[BLOCKCHAIN] Kafka consumer disabled (could not start)")

    async def stop(self):
        if self.enabled:
            try:
                await self.consumer.stop()
            finally:
                self.enabled = False

    async def run_forever(self):
        if not self.enabled:
            print("[BLOCKCHAIN] Consumer is disabled; run_forever will not start.")
            return

        async for msg in self.consumer:
            try:
                raw = msg.value.decode("utf-8")
                event = json.loads(raw)

                print(
                    f"[BLOCKCHAIN] Received topic={msg.topic} "
                    f"partition={msg.partition} offset={msg.offset} "
                    f"key={msg.key.decode('utf-8') if msg.key else None} "
                    f"event={event}"
                )

                block_hash = await self.ledger.store_block(event)
                print(f"[BLOCKCHAIN] Block stored hash={block_hash}")

            except json.JSONDecodeError as e:
                print(f"[BLOCKCHAIN] Invalid JSON: {repr(e)} raw={msg.value!r}")

            except Exception as e:
                print(f"[BLOCKCHAIN] Error processing message: {repr(e)}")
                traceback.print_exc()
