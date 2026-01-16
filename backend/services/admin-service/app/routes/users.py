from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.admin import AdminUserCreate, AdminUserResponse
from app.services.admin_service import AdminService
from app.deps.db import get_db

router = APIRouter()

@router.post("/", response_model=AdminUserResponse, status_code=status.HTTP_201_CREATED)
async def create_admin_user(
    user: AdminUserCreate,
    db: Session = Depends(get_db)
):
    """Create a new admin user"""
    admin_service = AdminService(db)
    existing = admin_service.get_by_email(user.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return admin_service.create_admin_user(user)

@router.get("/", response_model=List[AdminUserResponse])
async def list_admin_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List admin users"""
    admin_service = AdminService(db)
    return admin_service.list_admin_users(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=AdminUserResponse)
async def get_admin_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get admin user by ID"""
    admin_service = AdminService(db)
    user = admin_service.get_admin_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin user not found"
        )
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_admin_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Delete admin user"""
    admin_service = AdminService(db)
    user = admin_service.get_admin_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin user not found"
        )
    admin_service.delete_admin_user(user_id)
    return None
