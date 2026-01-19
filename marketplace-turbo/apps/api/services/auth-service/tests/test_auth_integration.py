import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_login():
    async with AsyncClient(app=app, base_url="http://test") as c:
        r = await c.post("/auth/register", json={"email":"a@a.com","password":"Password123!","role":"buyer"})
        assert r.status_code in (200, 409)
