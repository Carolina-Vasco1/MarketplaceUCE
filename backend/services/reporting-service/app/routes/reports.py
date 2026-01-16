from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.reporting import SalesReportResponse
from app.services.reporting_service import ReportingService
from app.deps.db import get_db

router = APIRouter()

@router.get("/sales/{seller_id}", response_model=List[SalesReportResponse])
async def get_seller_sales_reports(
    seller_id: str,
    period: str = "monthly",
    months: int = 12,
    db: Session = Depends(get_db)
):
    """Get sales reports for a seller"""
    reporting_service = ReportingService(db)
    return reporting_service.get_sales_reports(seller_id, period, months)

@router.get("/sales/{seller_id}/summary")
async def get_seller_sales_summary(
    seller_id: str,
    db: Session = Depends(get_db)
):
    """Get sales summary for a seller"""
    reporting_service = ReportingService(db)
    return reporting_service.get_sales_summary(seller_id)
