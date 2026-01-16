import json
from aiokafka import AIOKafkaConsumer

class NotificationConsumer:
    def __init__(self, bootstrap: str, group_id: str):
        self.consumer = AIOKafkaConsumer(
            "order.created",
            "payment.webhook.received",
            bootstrap_servers=bootstrap,
            group_id=group_id,
            auto_offset_reset="earliest",
        )

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def run_forever(self):
        async for msg in self.consumer:
            event = json.loads(msg.value.decode("utf-8"))
            # Aquí conectas email/SMS/push (SendGrid, SES, etc.)
            print(f"[notification] topic={msg.topic} event={event}")
