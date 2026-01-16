import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest

router = APIRouter(prefix="/api/v1/paypal", tags=["paypal"])

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET", "")

if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
    # No rompas el import, pero sí avisa cuando se use
    client = None
else:
    env = SandboxEnvironment(client_id=PAYPAL_CLIENT_ID, client_secret=PAYPAL_CLIENT_SECRET)
    client = PayPalHttpClient(env)

class CreateOrderIn(BaseModel):
    total: float
    currency: str = "USD"

class CaptureOrderIn(BaseModel):
    order_id: str

@router.post("/create-order")
async def create_order(body: CreateOrderIn):
    if client is None:
        raise HTTPException(status_code=500, detail="PayPal credentials missing (PAYPAL_CLIENT_ID/SECRET)")

    req = OrdersCreateRequest()
    req.prefer("return=representation")
    req.request_body({
        "intent": "CAPTURE",
        "purchase_units": [
            {"amount": {"currency_code": body.currency, "value": f"{body.total:.2f}"}}
        ],
    })

    try:
        res = client.execute(req)
        return {"id": res.result.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PayPal create-order error: {str(e)}")

@router.post("/capture-order")
async def capture_order(body: CaptureOrderIn):
    if client is None:
        raise HTTPException(status_code=500, detail="PayPal credentials missing (PAYPAL_CLIENT_ID/SECRET)")

    try:
        req = OrdersCaptureRequest(body.order_id)
        res = client.execute(req)
        return {"status": res.result.status, "result": res.result.__dict__}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PayPal capture-order error: {str(e)}")
