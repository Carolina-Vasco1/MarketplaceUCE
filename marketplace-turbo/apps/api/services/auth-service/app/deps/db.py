from __future__ import annotations

import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

POSTGRES_URL = os.getenv(
    "POSTGRES_URL",
    "postgresql+asyncpg://auth:auth@postgres:5432/auth_db",
)

engine = create_async_engine(POSTGRES_URL, pool_pre_ping=True)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

db = SessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
