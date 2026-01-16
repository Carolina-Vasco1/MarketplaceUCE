from __future__ import annotations

import os
import random
from datetime import datetime, timedelta, timezone

import jwt
import redis.asyncio as redis
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_db

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

OTP_TTL_SECONDS = 300  # 5 min


# ======================
# Helpers
# ======================
def _otp_key(email: str) -> str:
    return f"otp:{email.lower().strip()}"

def _make_otp() -> str:
    return f"{random.randint(0, 999999):06d}"

def _make_token(payload: dict) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=JWT_EXPIRES_MIN)
    to_encode = {**payload, "exp": exp}
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALG)

def _verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def _hash_password(plain: str) -> str:
    return pwd_ctx.hash(plain)


# ======================
# Schemas (inline, simple)
# ======================
from pydantic import BaseModel, EmailStr, Field

class OTPRequestIn(BaseModel):
    email: EmailStr

class OTPVerifyIn(BaseModel):
    email: EmailStr
    code: str = Field(min_length=6, max_length=6)

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)
    role: str = "buyer"  # buyer/seller/admin (admin solo por DB normalmente)

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
    Genera OTP y lo guarda en Redis.
    En local devolvemos el OTP en la respuesta (para pruebas).
    En prod: lo envías por correo/SMS.
    """
    email = body.email.lower().strip()
    code = _make_otp()
    await rds.set(_otp_key(email), code, ex=OTP_TTL_SECONDS)

    # DEV ONLY: devolver el código para probar
    return {"ok": True, "message": "OTP generated", "code_dev": code, "ttl_seconds": OTP_TTL_SECONDS}


@router.post("/verify-otp")
async def verify_otp(body: OTPVerifyIn):
    email = body.email.lower().strip()
    saved = await rds.get(_otp_key(email))
    if not saved:
        raise HTTPException(status_code=400, detail="OTP expired or not requested")
    if saved != body.code:
        raise HTTPException(status_code=400, detail="Invalid OTP code")

    # Marcamos como verificado por 10 min para permitir register
    await rds.set(f"otp_verified:{email}", "1", ex=600)
    return {"ok": True, "message": "OTP verified"}


@router.post("/register", response_model=TokenOut)
async def register(body: RegisterIn, db: AsyncSession = Depends(get_db)):
    email = body.email.lower().strip()

    # Exigir OTP verificado
    ok = await rds.get(f"otp_verified:{email}")
    if not ok:
        raise HTTPException(status_code=400, detail="OTP not verified")

    # Insert user (si no existe)
    # Nota: tu tabla es users(email, password_hash, role, is_active, created_at)
    try:
        # Ver si existe
        r = await db.execute(text("SELECT id FROM users WHERE email=:email"), {"email": email})
        row = r.first()
        if row:
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

    # limpiar flag OTP
    await rds.delete(f"otp_verified:{email}")
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
