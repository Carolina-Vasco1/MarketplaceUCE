from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.services.reporting_service import ReportingService
from app.deps.db import get_db

router = APIRouter()

@router.get("/dashboard")
async def get_analytics_dashboard(
    period: str = Query("monthly", regex="^(daily|weekly|monthly|yearly)$"),
    db: Session = Depends(get_db)
):
    """Get analytics dashboard data"""
    reporting_service = ReportingService(db)
    return reporting_service.get_dashboard_analytics(period)

@router.get("/user-growth")
async def get_user_growth(
    period: str = Query("monthly"),
    db: Session = Depends(get_db)
):
    """Get user growth metrics"""
    return {
        "period": period,
        "new_users": 500,
        "active_users": 5000,
        "churn_rate": 2.5
    }

@router.get("/traffic")
async def get_traffic_metrics(
    period: str = Query("daily"),
    db: Session = Depends(get_db)
):
    """Get traffic analytics"""
    return {
        "period": period,
        "page_views": 100000,
        "unique_visitors": 50000,
        "bounce_rate": 35.5
    }

@router.get("/conversion")
async def get_conversion_metrics(
    period: str = Query("monthly"),
    db: Session = Depends(get_db)
):
    """Get conversion metrics"""
    return {
        "period": period,
        "total_visitors": 50000,
        "total_conversions": 2500,
        "conversion_rate": 5.0
    }
