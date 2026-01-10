from fastapi import APIRouter, Header, HTTPException
from ..core.config import settings
from ..messaging.kafka import KafkaBus

router = APIRouter(prefix="/paypal", tags=["paypal"])
bus = KafkaBus(settings.KAFKA_BOOTSTRAP)

@router.post("/webhook")
async def paypal_webhook(payload: dict,
                         paypal_transmission_id: str = Header(default=""),
                         paypal_transmission_sig: str = Header(default="")):
    # Base segura: si falta transmission id -> 400
    if not paypal_transmission_id:
        raise HTTPException(400, "Missing PayPal transmission id")

    # En prod: verificar firma con endpoint /v1/notifications/verify-webhook-signature
    # usando PAYPAL_WEBHOOK_ID, paypal_transmission_sig, etc.

    event_type = payload.get("event_type", "UNKNOWN")
    resource = payload.get("resource", {})

    await bus.publish("payment.webhook.received", {
        "event_type": event_type,
        "resource": resource,
        "transmission_id": paypal_transmission_id,
    })
    return {"ok": True}

