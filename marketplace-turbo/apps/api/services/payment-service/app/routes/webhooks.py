from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from ..core.config import settings
from ..messaging.kafka import KafkaBus

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])
bus = KafkaBus(settings.KAFKA_BOOTSTRAP)

class PaymentData(BaseModel):
    paypal_order_id: str
    items: list
    customer: dict
    total_price: float
    payment_status: str

@router.post("/process")
async def process_payment(payment: PaymentData):
    """Process PayPal payment and create order"""
    try:
        # Publish payment event to Kafka
        await bus.publish("payment.processed", {
            "paypal_order_id": payment.paypal_order_id,
            "items": payment.items,
            "customer": payment.customer,
            "total_price": payment.total_price,
            "status": payment.payment_status,
        })
        
        return {
            "status": "success",
            "paypal_order_id": payment.paypal_order_id,
            "message": "Payment processed successfully"
        }
    except Exception as e:
        raise HTTPException(500, f"Payment processing failed: {str(e)}")


@router.post("/webhook")
async def paypal_webhook(payload: dict,
                         paypal_transmission_id: str = Header(default=""),
                         paypal_transmission_sig: str = Header(default="")):
    """Handle PayPal webhook events"""
    if not paypal_transmission_id:
        raise HTTPException(400, "Missing PayPal transmission id")

    event_type = payload.get("event_type", "UNKNOWN")
    resource = payload.get("resource", {})

    await bus.publish("payment.webhook.received", {
        "event_type": event_type,
        "resource": resource,
        "transmission_id": paypal_transmission_id,
    })
    return {"ok": True}


@router.get("/status/{paypal_order_id}")
async def get_payment_status(paypal_order_id: str):
    """Get payment status by PayPal order ID"""
    return {
        "paypal_order_id": paypal_order_id,
        "status": "completed"
    }

