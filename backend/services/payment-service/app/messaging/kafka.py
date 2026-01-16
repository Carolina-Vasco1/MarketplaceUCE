from aiokafka import AIOKafkaProducer
import json

class KafkaBus:
    def __init__(self, bootstrap: str):
        self.bootstrap = bootstrap
        self.producer: AIOKafkaProducer | None = None

    async def start(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap)
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def publish(self, topic: str, payload: dict):
        assert self.producer
        await self.producer.send_and_wait(topic, json.dumps(payload).encode("utf-8"))
