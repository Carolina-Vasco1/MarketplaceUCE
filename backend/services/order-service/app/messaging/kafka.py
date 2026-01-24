import json
from aiokafka import AIOKafkaProducer


class KafkaBus:
    def __init__(self, bootstrap: str):
        self.bootstrap = bootstrap
        self.producer: AIOKafkaProducer | None = None
        self.enabled = False

    async def start(self):
        # Si falla, NO mates el servicio
        try:
            self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap)
            await self.producer.start()
            self.enabled = True
            print(f"[KAFKA] Connected ✅ bootstrap={self.bootstrap}")
        except Exception as e:
            self.enabled = False
            self.producer = None
            print(f"[KAFKA] Disabled ❌ bootstrap={self.bootstrap} error={repr(e)}")

    async def stop(self):
        try:
            if self.producer:
                await self.producer.stop()
        finally:
            self.enabled = False
            self.producer = None

    async def publish(self, topic: str, payload: dict):
        if not self.enabled or not self.producer:
            print(f"[KAFKA disabled] skip publish topic={topic} payload={payload}")
            return

        data = json.dumps(payload).encode("utf-8")
        await self.producer.send_and_wait(topic, data)
