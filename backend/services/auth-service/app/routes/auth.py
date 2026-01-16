from __future__ import annotations

import os
import random
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
import redis.asyncio as redis
from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_db
from app.services.email_service import EmailService

router = APIRouter(prefix="/auth", tags=["auth"])

# ======================
# Config
# ======================
JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret_change_me")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
JWT_EXPIRES_MIN = int(os.getenv("JWT_EXPIRES_MIN", "1440"))

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
rds = redis.from_url(REDIS_URL, decode_responses=True)

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

OTP_TTL_SECONDS = int(os.getenv("OTP_TTL_SECONDS", "300"))  # 5 min
OTP_VERIFIED_TTL = int(os.getenv("OTP_VERIFIED_TTL", "600"))  # 10 min

email_service = EmailService()

# ======================
# Helpers
# ======================
def _otp_key(email: str) -> str:
    return f"otp:{email.lower().strip()}"

def _otp_verified_key(email: str) -> str:
    return f"otp_verified:{email.lower().strip()}"

def _make_otp() -> str:
    return f"{random.randint(0, 999999):06d}"

def _hash_password(plain: str) -> str:
    return pwd_ctx.hash(plain)

def _verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def _make_token(payload: dict) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=JWT_EXPIRES_MIN)
    to_encode = {**payload, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALG)

# ======================
# Schemas
# ======================
class OTPRequestIn(BaseModel):
    email: EmailStr

class OTPVerifyIn(BaseModel):
    email: EmailStr
    # ✅ acepta "code" o "otp"
    code: str = Field(min_length=6, max_length=6, alias="otp")

    class Config:
        populate_by_name = True

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)
    role: str = "buyer"  # buyer/seller/admin (admin idealmente solo por DB)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ======================
# Endpoints
# ======================

@router.post("/request-otp")
async def request_otp(body: OTPRequestIn):
    """
    Genera OTP, lo guarda en Redis y lo envía por correo.
    """
    email = body.email.lower().strip()
    code = _make_otp()

    await rds.set(_otp_key(email), code, ex=OTP_TTL_SECONDS)

    # ✅ enviar correo (si falla, te muestra error real)
    try:
        email_service.send_otp(email, code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SMTP error: {str(e)}")

    return {"ok": True, "message": "OTP sent. Check your email."}


@router.post("/verify-otp")
async def verify_otp(body: OTPVerifyIn):
    email = body.email.lower().strip()

    saved = await rds.get(_otp_key(email))
    if not saved:
        raise HTTPException(status_code=400, detail="OTP expired or not requested")

    # body.code acepta "code" o "otp"
    if saved != body.code:
        raise HTTPException(status_code=400, detail="Invalid OTP code")

    # ✅ marcado como verificado para permitir register
    await rds.set(_otp_verified_key(email), "1", ex=OTP_VERIFIED_TTL)
    return {"ok": True, "message": "OTP verified"}


@router.post("/register", response_model=TokenOut)
async def register(body: RegisterIn, db: AsyncSession = Depends(get_db)):
    email = body.email.lower().strip()

    ok = await rds.get(_otp_verified_key(email))
    if not ok:
        raise HTTPException(status_code=400, detail="OTP not verified")

    # Crear usuario si no existe
    try:
        r = await db.execute(text("SELECT id FROM users WHERE email=:email"), {"email": email})
        if r.first():
            raise HTTPException(status_code=409, detail="Email already registered")

        pw_hash = _hash_password(body.password)

        await db.execute(
            text("""
                INSERT INTO users (email, password_hash, role, is_active)
                VALUES (:email, :ph, :role, true)
            """),
            {"email": email, "ph": pw_hash, "role": body.role},
        )
        await db.commit()

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Register error: {str(e)}")

    # limpiar flags OTP
    await rds.delete(_otp_verified_key(email))
    await rds.delete(_otp_key(email))

    token = _make_token({"sub": email, "role": body.role})
    return TokenOut(access_token=token)


@router.post("/login", response_model=TokenOut)
async def login(body: LoginIn, db: AsyncSession = Depends(get_db)):
    email = body.email.lower().strip()

    try:
        r = await db.execute(
            text("SELECT id, email, password_hash, role, is_active FROM users WHERE email=:email"),
            {"email": email},
        )
        row = r.mappings().first()
        if not row:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not row["is_active"]:
            raise HTTPException(status_code=403, detail="User is inactive")

        if not _verify_password(body.password, row["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = _make_token({"sub": row["email"], "role": row["role"], "uid": str(row["id"])})
        return TokenOut(access_token=token)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")
