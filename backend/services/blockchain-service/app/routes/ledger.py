from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.db.session import async_session
from app.db.models import LedgerBlock

router = APIRouter()

@router.get("/blocks")
async def list_blocks(limit: int = 20):
    async with async_session() as session:
        result = await session.execute(
            select(LedgerBlock).order_by(LedgerBlock.created_at.desc()).limit(limit)
        )
        blocks = result.scalars().all()

    return [
        {
            "order_id": b.order_id,
            "hash": b.hash,
            "payload": b.payload,
            "created_at": b.created_at,
        }
        for b in blocks
    ]

@router.get("/blocks/{order_id}")
async def get_block(order_id: str):
    async with async_session() as session:
        result = await session.execute(
            select(LedgerBlock).where(LedgerBlock.order_id == order_id)
        )
        block = result.scalar_one_or_none()

    if not block:
        raise HTTPException(status_code=404, detail="Block not found")

    return {
        "order_id": block.order_id,
        "hash": block.hash,
        "payload": block.payload,
        "created_at": block.created_at,
    }
