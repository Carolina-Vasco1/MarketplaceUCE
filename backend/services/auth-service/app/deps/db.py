from __future__ import annotations
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import make_engine, make_session_factory

POSTGRES_URL = os.getenv(
    "POSTGRES_URL",
    "postgresql+asyncpg://auth:auth@postgres:5432/auth_db",
)

_engine = make_engine(POSTGRES_URL)
_SessionLocal = make_session_factory(_engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with _SessionLocal() as session:
        yield session
