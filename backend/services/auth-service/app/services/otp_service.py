import random
import time
import redis.asyncio as redis
from app.core.config import settings

class OTPService:
    def __init__(self, r: redis.Redis):
        self.r = r

    def _key_code(self, email: str) -> str:
        return f"otp:code:{email}"

    def _key_last(self, email: str) -> str:
        return f"otp:last:{email}"

    def _key_verified(self, email: str) -> str:
        return f"otp:verified:{email}"

    async def can_resend(self, email: str) -> bool:
        last = await self.r.get(self._key_last(email))
        if not last:
            return True
        return (time.time() - float(last)) >= settings.OTP_RESEND_COOLDOWN

    async def request_otp(self, email: str) -> str:
        code = f"{random.randint(0, 999999):06d}"
        await self.r.set(self._key_code(email), code, ex=settings.OTP_TTL_SECONDS)
        await self.r.set(self._key_last(email), str(time.time()), ex=settings.OTP_TTL_SECONDS)
        return code

    async def verify_otp(self, email: str, code: str) -> None:
        saved = await self.r.get(self._key_code(email))
        if not saved:
            raise ValueError("OTP expirado o no solicitado")
        if saved != code:
            raise ValueError("OTP incorrecto")

        # marca como verificado (para permitir /register)
        await self.r.set(self._key_verified(email), "1", ex=settings.OTP_VERIFIED_TTL)
        await self.r.delete(self._key_code(email))

    async def is_verified_recently(self, email: str) -> bool:
        v = await self.r.get(self._key_verified(email))
        return v == "1"
