import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def add_cors(app: FastAPI) -> None:
    origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

    allow_origins = [
        origin,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    allow_origins = list(dict.fromkeys(allow_origins))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,  # si usas auth por cookies; si no, igual no molesta
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
