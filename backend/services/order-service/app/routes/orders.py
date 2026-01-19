import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import SessionLocal
from ..db.models import Order
from ..schemas.order import OrderIn, OrderOut
from ..messaging.kafka import KafkaBus
from ..core.config import settings

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])
bus = KafkaBus(settings.KAFKA_BOOTSTRAP)

async def db() -> AsyncSession:
    async with SessionLocal() as s:
        yield s

# -----------------------------
# GET: Listar orders (para My Orders)
# -----------------------------
@router.get("", response_model=list[OrderOut])
@router.get("/", response_model=list[OrderOut])
async def list_orders(
    buyer_id: str | None = Query(None),
    status: str | None = Query(None),  # all/pending/created/confirmed/shipped/delivered/cancelled
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(db),
):
    stmt = select(Order).order_by(Order.id.desc())

    if buyer_id:
        stmt = stmt.where(Order.buyer_id == buyer_id)

    if status and status.lower() != "all":
        # tu DB hoy guarda "created", tu front usa "pending"
        s = status.lower()
        if s == "pending":
            s = "created"
        stmt = stmt.where(Order.status == s)

    stmt = stmt.limit(limit)

    rows = (await session.execute(stmt)).scalars().all()

    out: list[OrderOut] = []
    for o in rows:
        out.append(OrderOut(
            id=o.id,
            buyer_id=o.buyer_id,
            product_id=o.product_id,
            amount=float(o.amount),
            status=o.status,
        ))
    return out

# -----------------------------
# POST: crear order
# -----------------------------
async def _create_order(payload: OrderIn, session: AsyncSession) -> OrderOut:
    order_id = str(uuid.uuid4())
    order = Order(
        id=order_id,
        buyer_id=payload.buyer_id,
        product_id=payload.product_id,
        amount=float(payload.amount),
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
                "amount": float(payload.amount),
            },
        )
    except Exception as e:
        print("[ORDER] Kafka publish skipped:", repr(e))

    return OrderOut(id=order_id, **payload.model_dump(), status="created")

@router.post("", response_model=OrderOut)
@router.post("/", response_model=OrderOut)
async def create_order_v1(payload: OrderIn, session: AsyncSession = Depends(db)):
    return await _create_order(payload, session)

# -----------------------------
# Compat opcional (si algo usa /orders directo)
# -----------------------------
compat = APIRouter(tags=["orders-compat"])

@compat.post("/orders", response_model=OrderOut)
@compat.post("/orders/", response_model=OrderOut)
async def create_order_compat(payload: OrderIn, session: AsyncSession = Depends(db)):
    return await _create_order(payload, session)

@compat.post("/orders/buy")
async def buy(payload: dict, session: AsyncSession = Depends(db)):
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

@compat.post("/orders/create-from-cart")
async def create_order_from_cart(payload: dict, session: AsyncSession = Depends(db)):
    paypal_order_id = (payload.get("paypal_order_id") or "").strip()
    items = payload.get("items", [])
    customer = payload.get("customer", {})
    total_price = payload.get("total_price", 0)
    payment_status = (payload.get("payment_status") or "pending").strip()

    if not paypal_order_id or not items or not customer:
        raise HTTPException(400, "Missing required fields: paypal_order_id, items, customer")

    try:
        total_price = float(total_price)
    except:
        raise HTTPException(400, "total_price must be a number")

    order_id = str(uuid.uuid4())

    order = Order(
        id=order_id,
        buyer_id=customer.get("email", "unknown"),
        product_id=",".join([str(item.get("product_id", "")) for item in items]),
        amount=total_price,
        status=payment_status if payment_status != "pending" else "created",
    )
    session.add(order)
    await session.commit()

    try:
        await bus.publish(
            "order.created_from_cart",
            {
                "order_id": order_id,
                "paypal_order_id": paypal_order_id,
                "buyer_id": customer.get("email"),
                "items": items,
                "total_price": total_price,
                "customer": customer,
                "payment_status": payment_status,
            },
        )
    except Exception as e:
        print("[ORDER] Kafka publish skipped:", repr(e))

    return {"order_id": order_id, "paypal_order_id": paypal_order_id, "status": payment_status, "total_price": total_price}
