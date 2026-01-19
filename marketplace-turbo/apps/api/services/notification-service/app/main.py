from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Notification Service")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "notification-service"}


@app.post("/api/v1/notifications/send")
async def send_notification(data: dict):
    """Send notification"""
    return {"status": "sent", "notification": data}


@app.get("/api/v1/notifications/{user_id}")
async def get_notifications(user_id: str):
    """Get notifications for user"""
    return {"user_id": user_id, "notifications": []}
