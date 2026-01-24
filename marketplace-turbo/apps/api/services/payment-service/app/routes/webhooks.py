from datetime import datetime
from fastapi import APIRouter, Request, HTTPException

from app.messaging.kafka import get_bus

router = APIRouter(prefix="/api/v1/webhooks", tags=["webhooks"])


@router.post("/paypal")
async def paypal_webhook(request: Request):
    """
    Recibe webhooks de PayPal y publica un evento a Kafka.
    """
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    event_type = payload.get("event_type")
    resource = payload.get("resource") or {}

    # Ajusta los eventos reales que recibes
    if event_type in ("PAYMENT.CAPTURE.COMPLETED", "CHECKOUT.ORDER.APPROVED"):
        purchase_units = resource.get("purchase_units") or []
        amount_obj = (purchase_units[0].get("amount") if purchase_units else {}) or {}

        event = {
            "event": "payment.completed",
            "paypal_order_id": resource.get("id"),
            "amount": amount_obj.get("value"),
            "currency": amount_obj.get("currency_code"),
            "payer_email": (resource.get("payer") or {}).get("email_address"),
            "timestamp": datetime.utcnow().isoformat(),
            "raw": payload, 
        }

        await get_bus().publish("payment.completed", event)

    return {"ok": True, "event_type": event_type}
