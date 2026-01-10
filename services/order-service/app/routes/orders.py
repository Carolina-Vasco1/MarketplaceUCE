import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import SessionLocal
from ..db.models import Order
from ..schemas.order import OrderIn, OrderOut
from ..messaging.kafka import KafkaBus
from ..core.config import settings

router = APIRouter(prefix="/orders", tags=["orders"])
bus = KafkaBus(settings.KAFKA_BOOTSTRAP)

async def db() -> AsyncSession:
    async with SessionLocal() as s:
        yield s

@router.post("/", response_model=OrderOut)
async def create_order(payload: OrderIn, session: AsyncSession = Depends(db)):
    order_id = str(uuid.uuid4())
    order = Order(
        id=order_id,
        buyer_id=payload.buyer_id,
        product_id=payload.product_id,
        amount=payload.amount,
        status="created",
    )
    session.add(order)
    await session.commit()

    await bus.publish("order.created", {
        "order_id": order_id,
        "buyer_id": payload.buyer_id,
        "product_id": payload.product_id,
        "amount": payload.amount
    })
    return OrderOut(id=order_id, **payload.model_dump(), status="created")
