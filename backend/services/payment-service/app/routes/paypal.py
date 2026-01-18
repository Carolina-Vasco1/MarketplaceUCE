from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest

from app.core.config import settings

router = APIRouter(prefix="/api/v1/paypal", tags=["paypal"])


def get_paypal_client() -> PayPalHttpClient:
    """
    Crea el cliente en runtime (no en import-time).
    Soporta sandbox o live según PAYPAL_ENV.
    """
    if not settings.PAYPAL_CLIENT_ID or not settings.PAYPAL_CLIENT_SECRET:
        raise HTTPException(
            status_code=500,
            detail="PayPal credentials missing (PAYPAL_CLIENT_ID / PAYPAL_CLIENT_SECRET)"
        )

    env_name = (getattr(settings, "PAYPAL_ENV", "sandbox") or "sandbox").lower()

    if env_name == "live":
        env = LiveEnvironment(
            client_id=settings.PAYPAL_CLIENT_ID,
            client_secret=settings.PAYPAL_CLIENT_SECRET,
        )
    else:
        env = SandboxEnvironment(
            client_id=settings.PAYPAL_CLIENT_ID,
            client_secret=settings.PAYPAL_CLIENT_SECRET,
        )

    return PayPalHttpClient(env)


class CreateOrderIn(BaseModel):
    total: float = Field(..., gt=0)
    currency: str = "USD"


class CaptureOrderIn(BaseModel):
    order_id: str


@router.get("/health")
async def paypal_health():
    # Simple para saber si lee env vars
    return {
        "ok": True,
        "env": getattr(settings, "PAYPAL_ENV", "sandbox"),
        "client_id_present": bool(settings.PAYPAL_CLIENT_ID),
    }


@router.post("/create-order")
async def create_order(body: CreateOrderIn):
    client = get_paypal_client()

    req = OrdersCreateRequest()
    req.prefer("return=representation")
    req.request_body({
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": body.currency,
                    "value": f"{body.total:.2f}"
                }
            }
        ],
    })

    try:
        res = client.execute(req)
        return {"id": res.result.id, "status": res.result.status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PayPal create-order error: {str(e)}")


@router.post("/capture-order")
async def capture_order(body: CaptureOrderIn):
    client = get_paypal_client()

    try:
        req = OrdersCaptureRequest(body.order_id)
        res = client.execute(req)
        return {"status": res.result.status, "id": getattr(res.result, "id", body.order_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PayPal capture-order error: {str(e)}")
