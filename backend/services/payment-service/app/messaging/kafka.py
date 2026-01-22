import json
from typing import Optional
from aiokafka import AIOKafkaProducer


class KafkaBus:
    def __init__(self, bootstrap: str):
        self.bootstrap = bootstrap
        self.producer: Optional[AIOKafkaProducer] = None

    async def start(self):
        if self.producer is not None:
            return
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap)
        await self.producer.start()
        print(f"[KAFKA] Producer connected ✅ bootstrap={self.bootstrap}")

    async def stop(self):
        if self.producer is not None:
            await self.producer.stop()
            self.producer = None
            print("[KAFKA] Producer stopped ✅")

    async def publish(self, topic: str, payload: dict):
        if self.producer is None:
            raise RuntimeError("Kafka producer is not started")
        data = json.dumps(payload).encode("utf-8")
        await self.producer.send_and_wait(topic, data)


_bus: Optional[KafkaBus] = None


def init_bus(bootstrap: str) -> KafkaBus:
    global _bus
    if _bus is None:
        _bus = KafkaBus(bootstrap=bootstrap)
    return _bus


def get_bus() -> KafkaBus:
    if _bus is None:
        raise RuntimeError("Kafka bus not initialized. Call init_bus() first.")
    return _bus
