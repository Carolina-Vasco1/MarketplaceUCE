import hashlib
import json
from datetime import datetime

from app.db.session import async_session
from app.db.models import LedgerBlock

class LedgerService:
    async def store_block(self, event: dict):
        payload = json.dumps(event, sort_keys=True)
        block_hash = hashlib.sha256(payload.encode()).hexdigest()

        async with async_session() as session:
            block = LedgerBlock(
                order_id=event.get("paypal_order_id") or event.get("order_id"),
                hash=block_hash,
                payload=event,
                created_at=datetime.utcnow()
            )
            session.add(block)
            await session.commit()

        print(f"[BLOCKCHAIN] Block stored ✅ hash={block_hash}")
        return block_hash
