import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def add_cors(app: FastAPI) -> None:
    origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin, "http://localhost:5173"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
