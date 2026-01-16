from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.paypal import router as paypal_router

app = FastAPI(title="Payment Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(paypal_router)
