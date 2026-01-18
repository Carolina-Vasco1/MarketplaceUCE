from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.paypal import router as paypal_router
from app.routes.webhooks import router as payments_router  # si este archivo se llama webhooks.py

app = FastAPI(title="Payment Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(paypal_router)
app.include_router(payments_router)
