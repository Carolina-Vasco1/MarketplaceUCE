from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os

router = APIRouter(prefix="/api/v1/config", tags=["config"])


@router.get("/paypal")
async def get_paypal_config():
    """Get PayPal configuration for frontend"""
    # Use sandbox client-id for development
    client_id = os.getenv(
        "PAYPAL_CLIENT_ID",
        "AQc_rjH8LzqYhb7ThvI9oCpQxV4K5p0VBgZqJ3qJ3q3qJ3qJ3q"
    )
    
    return JSONResponse({
        "client_id": client_id,
        "environment": "sandbox" if "AQc_" in client_id else "production"
    })
