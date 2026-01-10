from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis

from app.deps.db import db
from app.schemas.auth import OTPRequestIn, OTPVerifyIn, RegisterIn, LoginIn, TokenOut
from app.core.validators import validate_institutional_email
from app.core.config import settings
from app.services.email_service import EmailService
from app.services.otp_service import OTPService
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


def redis_client() -> redis.Redis:
    return redis.from_url(settings.REDIS_URL, decode_responses=True)


@router.post("/request-otp")
async def request_otp(payload: OTPRequestIn):
    try:
        validate_institutional_email(payload.email)
        email = payload.email.lower().strip()

        r = redis_client()
        otp = OTPService(r)

        if not await otp.can_resend(email):
            raise ValueError("Espera 60s para solicitar otro OTP")

        code = await otp.request_otp(email)
        EmailService().send_otp(email, code)

        return {"ok": True, "message": "OTP enviado al correo institucional (o impreso en logs en modo DEV)"}

    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        print("[ERROR request_otp]", repr(e))
        raise HTTPException(500, "Error interno solicitando OTP (revisa logs del auth-service)")


@router.post("/verify-otp")
async def verify_otp(payload: OTPVerifyIn):
    try:
        validate_institutional_email(payload.email)
        email = payload.email.lower().strip()

        r = redis_client()
        otp = OTPService(r)

        await otp.verify_otp(email, payload.code)
        return {"ok": True, "message": "Correo verificado. Ya puedes registrarte."}

    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        print("[ERROR verify_otp]", repr(e))
        raise HTTPException(500, "Error interno verificando OTP (revisa logs)")


@router.post("/register", response_model=TokenOut)
async def register(payload: RegisterIn, session: AsyncSession = Depends(db)):
    try:
        validate_institutional_email(payload.email)
        email = payload.email.lower().strip()

        r = redis_client()
        otp = OTPService(r)
        if not await otp.is_verified_recently(email):
            raise ValueError("Primero verifica tu correo con OTP")

        token = await UserService.register(session, email, payload.password, payload.role)
        return TokenOut(access_token=token)

    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        print("[ERROR register]", repr(e))
        raise HTTPException(500, "Error interno registrando (revisa logs)")


@router.post("/login", response_model=TokenOut)
async def login(payload: LoginIn, session: AsyncSession = Depends(db)):
    try:
        validate_institutional_email(payload.email)
        email = payload.email.lower().strip()

        token = await UserService.login(session, email, payload.password)
        return TokenOut(access_token=token)

    except ValueError as e:
        raise HTTPException(401, str(e))
    except Exception as e:
        print("[ERROR login]", repr(e))
        raise HTTPException(500, "Error interno en login (revisa logs)")
