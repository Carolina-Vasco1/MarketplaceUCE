from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from pydantic import BaseModel

from app.deps.db import get_db

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

class RoleIn(BaseModel):
    role: str

class ActiveIn(BaseModel):
    is_active: bool

@router.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        text("SELECT id, email, role, is_active, created_at FROM users ORDER BY id DESC")
    )
    return res.mappings().all()

@router.patch("/users/{user_id}/role")
async def set_user_role(user_id: int, body: RoleIn, db: AsyncSession = Depends(get_db)):
    if body.role not in ["buyer", "seller", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    res = await db.execute(
        text("UPDATE users SET role=:role WHERE id=:id RETURNING id, email, role, is_active, created_at"),
        {"role": body.role, "id": user_id},
    )
    row = res.mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    await db.commit()
    return row

@router.patch("/users/{user_id}/active")
async def set_user_active(user_id: int, body: ActiveIn, db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        text("UPDATE users SET is_active=:a WHERE id=:id RETURNING id, email, role, is_active, created_at"),
        {"a": body.is_active, "id": user_id},
    )
    row = res.mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    await db.commit()
    return row
