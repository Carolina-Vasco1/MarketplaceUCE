from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.admin import AdminUserResponse
from app.services.admin_service import AdminService
from app.deps.db import get_db

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard(db: Session = Depends(get_db)):
    """Get admin dashboard statistics"""
    admin_service = AdminService(db)
    return {
        "total_users": 1000,
        "total_products": 5000,
        "total_orders": 2000,
        "pending_reports": 50,
        "revenue": 100000.00
    }

@router.get("/settings")
async def get_settings(db: Session = Depends(get_db)):
    """Get admin settings"""
    return {
        "commission_rate": 10,
        "min_withdrawal": 50,
        "max_product_images": 5,
        "maintenance_mode": False
    }

@router.put("/settings")
async def update_settings(settings: dict, db: Session = Depends(get_db)):
    """Update admin settings"""
    return {"message": "Settings updated successfully"}
