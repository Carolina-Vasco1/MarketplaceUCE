import pytest
import redis.asyncio as redis
from app.services.otp_service import OTPService
from app.core.config import settings

@pytest.mark.asyncio
async def test_otp_flow():
    r = redis.from_url(settings.REDIS_URL, decode_responses=True)
    otp = OTPService(r)

    email = "user@uce.edu.ec"
    code = await otp.request_otp(email)
    await otp.verify_otp(email, code)
    assert await otp.is_verified_recently(email) is True
