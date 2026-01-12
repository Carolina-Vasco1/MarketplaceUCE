import uuid
from fastapi import APIRouter, Depends, HTTPException
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

    try:
        await bus.publish(
            "order.created",
            {
                "order_id": order_id,
                "buyer_id": payload.buyer_id,
                "product_id": payload.product_id,
                "amount": payload.amount,
            },
        )
    except Exception as e:
        print("[ORDER] Kafka publish skipped:", repr(e))

    return OrderOut(id=order_id, **payload.model_dump(), status="created")


@router.post("/buy")
async def buy(payload: dict, session: AsyncSession = Depends(db)):
    try:
        buyer_id = (payload.get("buyer_id") or "").strip()
        product_id = (payload.get("product_id") or "").strip()
        amount = payload.get("amount")

        if not buyer_id or not product_id or amount is None:
            raise HTTPException(400, "buyer_id, product_id and amount are required")

        try:
            amount = float(amount)
        except:
            raise HTTPException(400, "amount must be a number")

        if amount <= 0:
            raise HTTPException(400, "amount must be > 0")

        order_id = str(uuid.uuid4())
        order = Order(
            id=order_id,
            buyer_id=buyer_id,
            product_id=product_id,
            amount=amount,
            status="created",
        )
        session.add(order)
        await session.commit()

        try:
            await bus.publish(
                "order.created",
                {
                    "order_id": order_id,
                    "buyer_id": buyer_id,
                    "product_id": product_id,
                    "amount": amount,
                },
            )
        except Exception as e:
            print("[ORDER] Kafka publish skipped:", repr(e))

        return {"order_id": order_id, "status": "created"}

    except HTTPException:
        raise
    except Exception as e:
        print("[ERROR /orders/buy]", repr(e))
        raise HTTPException(500, "Order service internal error (check order-service logs)")
