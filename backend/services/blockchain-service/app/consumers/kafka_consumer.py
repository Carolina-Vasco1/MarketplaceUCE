import json
import time
import hashlib
from aiokafka import AIOKafkaConsumer
from sqlalchemy import select, desc
from app.core.config import settings
from app.db.session import SessionLocal
from app.db.models import LedgerBlock

GENESIS_PREV = "0" * 64

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def compute_block_hash(index: int, prev_hash: str, topic: str, event_type: str, ts_ms: int, payload_json: str) -> str:
    base = f"{index}|{prev_hash}|{topic}|{event_type}|{ts_ms}|{payload_json}"
    return sha256_hex(base)

class BlockchainConsumer:
    def __init__(self):
        topics = [t.strip() for t in settings.KAFKA_TOPICS.split(",") if t.strip()]
        self.topics = topics
        self.consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP,
            group_id="blockchain-ledger",
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )

    async def start(self):
        await self.consumer.start()
        print(f"[BLOCKCHAIN] Kafka consumer started topics={self.topics}")

    async def stop(self):
        await self.consumer.stop()
        print("[BLOCKCHAIN] Kafka consumer stopped")

    async def _append_block(self, topic: str, payload: dict):
        # Normaliza payload a JSON determinístico (para recomputar hash igual)
        payload_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        ts_ms = int(time.time() * 1000)

        async with SessionLocal() as session:
            last = (await session.execute(select(LedgerBlock).order_by(desc(LedgerBlock.index)).limit(1))).scalars().first()
            next_index = (last.index + 1) if last else 1
            prev_hash = last.hash if last else GENESIS_PREV

            event_type = payload.get("event_type") or topic

            h = compute_block_hash(next_index, prev_hash, topic, event_type, ts_ms, payload_json)

            b = LedgerBlock(
                index=next_index,
                prev_hash=prev_hash,
                hash=h,
                topic=topic,
                event_type=str(event_type),
                payload_json=payload_json,
                ts_ms=ts_ms,
            )
            session.add(b)
            await session.commit()

        print(f"[BLOCKCHAIN] appended index={next_index} topic={topic}")

    async def run_forever(self):
        async for msg in self.consumer:
            try:
                raw = msg.value.decode("utf-8")
                payload = json.loads(raw)
            except Exception:
                payload = {"raw": str(msg.value)}

            await self._append_block(msg.topic, payload)
