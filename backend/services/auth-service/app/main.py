from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.admin_users import router as admin_users_router

from app.routes.auth import router as auth_router

app = FastAPI(title="Auth Service", version="1.0.0")
app.include_router(admin_users_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
