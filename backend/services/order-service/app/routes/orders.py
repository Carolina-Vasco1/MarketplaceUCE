import uuid
from fastapi import APIRouter, Depends, Header, HTTPException, Path, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import settings
from ..db.models import Order
from ..db.session import SessionLocal
from ..messaging.kafka import KafkaBus
from ..schemas.order import OrderIn, OrderOut

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])
compat = APIRouter(prefix="/orders", tags=["orders-compat"])
bus = KafkaBus(settings.KAFKA_BOOTSTRAP)

async def db() -> AsyncSession:
    async with SessionLocal() as s:
        yield s

def norm_email(v: str | None) -> str:
    return (v or "").strip().lower()

def norm_status(v: str | None) -> str | None:
    if not v:
        return None
    s = v.strip().lower()
    if s == "all":
        return None
    if s == "pending":
        return "created"
    return s


@router.get("", response_model=list[OrderOut])
@router.get("/", response_model=list[OrderOut])
async def list_orders(
    buyer_id: str | None = Query(None),
    status: str | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(db),
):
    stmt = select(Order).order_by(Order.id.desc())

    if buyer_id:
        stmt = stmt.where(Order.buyer_id == norm_email(buyer_id))

    s = norm_status(status)
    if s:
        stmt = stmt.where(Order.status == s)

    rows = (await session.execute(stmt.limit(limit))).scalars().all()

    return [
        OrderOut(
            id=o.id,
            buyer_id=o.buyer_id,
            product_id=o.product_id,
            amount=float(o.amount),
            status=o.status,
        )
        for o in rows
    ]


@router.get("/me", response_model=list[OrderOut])
async def my_orders(
    status: str | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    x_user_email: str | None = Header(default=None),
    session: AsyncSession = Depends(db),
):
    email = norm_email(x_user_email)
    if not email:
        raise HTTPException(401, "Missing X-User-Email")

    stmt = select(Order).where(Order.buyer_id == email).order_by(Order.id.desc())

    s = norm_status(status)
    if s:
        stmt = stmt.where(Order.status == s)

    rows = (await session.execute(stmt.limit(limit))).scalars().all()

    return [
        OrderOut(
            id=o.id,
            buyer_id=o.buyer_id,
            product_id=o.product_id,
            amount=float(o.amount),
            status=o.status,
        )
        for o in rows
    ]


async def _create_order(payload: OrderIn, session: AsyncSession) -> OrderOut:
    order_id = str(uuid.uuid4())
    buyer = norm_email(payload.buyer_id)

    order = Order(
        id=order_id,
        buyer_id=buyer,
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
                "buyer_id": buyer,
                "product_id": payload.product_id,
                "amount": float(payload.amount),
            },
        )
    except Exception:
        pass

    return OrderOut(
        id=order_id,
        buyer_id=buyer,
        product_id=payload.product_id,
        amount=float(payload.amount),
        status="created",
    )


@router.post("", response_model=OrderOut)
@router.post("/", response_model=OrderOut)
async def create_order_v1(payload: OrderIn, session: AsyncSession = Depends(db)):
    return await _create_order(payload, session)


@router.post("/buy")
async def buy_v1(
    payload: dict,
    x_user_email: str | None = Header(default=None),
    session: AsyncSession = Depends(db),
):
    buyer_id = norm_email(payload.get("buyer_id"))
    if not buyer_id:
        buyer_id = norm_email(x_user_email)

    product_id = (payload.get("product_id") or "").strip()
    amount = payload.get("amount")

    if not buyer_id or not product_id or amount is None:
        raise HTTPException(400, "buyer_id (or X-User-Email), product_id and amount are required")

    try:
        amount = float(amount)
    except Exception:
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
    except Exception:
        pass

    return {"order_id": order_id, "status": "created"}


# ✅ ESTE ES EL QUE TE FALTABA (para el cart)
@router.post("/create-from-cart")
async def create_from_cart_v1(
    payload: dict,
    x_user_email: str | None = Header(default=None),
    session: AsyncSession = Depends(db),
):
    paypal_order_id = (payload.get("paypal_order_id") or "").strip()
    items = payload.get("items", []) or []
    customer = payload.get("customer", {}) or {}
    total_price = payload.get("total_price", 0)
    payment_status = (payload.get("payment_status") or "pending").strip().lower()

    # ✅ para que el buyer vea sus orders aunque el email de PayPal sea distinto
    buyer_email = norm_email(x_user_email) or norm_email(customer.get("email"))

    if not paypal_order_id or not items or not buyer_email:
        raise HTTPException(400, "Missing required fields: paypal_order_id, items, buyer email")

    try:
        total_price = float(total_price)
    except Exception:
        raise HTTPException(400, "total_price must be a number")

    order_id = str(uuid.uuid4())

    product_ids = ",".join(
        [str(i.get("product_id", "")).strip() for i in items if i.get("product_id")]
    )

    order = Order(
        id=order_id,
        buyer_id=buyer_email,
        product_id=product_ids,
        amount=total_price,
        status="created" if payment_status == "pending" else payment_status,
    )
    session.add(order)
    await session.commit()

    try:
        await bus.publish(
            "order.created_from_cart",
            {
                "order_id": order_id,
                "paypal_order_id": paypal_order_id,
                "buyer_id": buyer_email,
                "items": items,
                "total_price": total_price,
                "customer": customer,
                "payment_status": payment_status,
            },
        )
    except Exception:
        pass

    return {"order_id": order_id, "paypal_order_id": paypal_order_id, "status": order.status, "total_price": total_price}


# ✅ IMPORTANTE: esto va al final
@router.get("/{order_id}", response_model=OrderOut)
async def get_order_by_id(
    order_id: str = Path(..., min_length=1),
    x_user_email: str | None = Header(default=None),
    session: AsyncSession = Depends(db),
):
    o = await session.get(Order, order_id)
    if not o:
        raise HTTPException(404, "Order not found")

    email = norm_email(x_user_email)
    if email and norm_email(o.buyer_id) != email:
        raise HTTPException(403, "Forbidden")

    return OrderOut(
        id=o.id,
        buyer_id=o.buyer_id,
        product_id=o.product_id,
        amount=float(o.amount),
        status=o.status,
    )


# ---------- compat ----------
@compat.post("", response_model=OrderOut)
@compat.post("/", response_model=OrderOut)
async def create_order_compat(payload: OrderIn, session: AsyncSession = Depends(db)):
    return await _create_order(payload, session)

@compat.post("/buy")
async def buy_compat(
    payload: dict,
    x_user_email: str | None = Header(default=None),
    session: AsyncSession = Depends(db),
):
    return await buy_v1(payload, x_user_email=x_user_email, session=session)
