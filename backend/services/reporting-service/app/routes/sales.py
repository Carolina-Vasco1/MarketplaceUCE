from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas.reporting import SalesReportResponse
from app.services.reporting_service import ReportingService
from app.deps.db import get_db

router = APIRouter()

@router.get("/by-seller/{seller_id}")
async def get_seller_sales_metrics(
    seller_id: str,
    start_date: str = Query(None),
    end_date: str = Query(None),
    db: Session = Depends(get_db)
):
    """Get sales metrics for a seller"""
    reporting_service = ReportingService(db)
    return reporting_service.get_sales_metrics(seller_id, start_date, end_date)

@router.get("/by-product/{product_id}")
async def get_product_sales(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Get sales data for a product"""
    return {
        "product_id": product_id,
        "total_sold": 150,
        "total_revenue": 15000.00,
        "avg_price": 100.00
    }

@router.get("/platform/summary")
async def get_platform_sales_summary(db: Session = Depends(get_db)):
    """Get overall platform sales summary"""
    reporting_service = ReportingService(db)
    return reporting_service.get_platform_summary()
