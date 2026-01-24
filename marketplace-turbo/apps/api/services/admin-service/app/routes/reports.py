from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.admin import ReportCreate, ReportResponse
from app.services.admin_service import AdminService
from app.deps.db import get_db

router = APIRouter()

@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    report: ReportCreate,
    db: Session = Depends(get_db)
):
    """Create a new report"""
    if not report.reported_user_id and not report.reported_product_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either user_id or product_id must be provided"
        )
    admin_service = AdminService(db)
    return admin_service.create_report(report)

@router.get("/", response_model=List[ReportResponse])
async def list_reports(
    status: str = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List reports"""
    admin_service = AdminService(db)
    return admin_service.list_reports(status=status, skip=skip, limit=limit)

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    db: Session = Depends(get_db)
):
    """Get report by ID"""
    admin_service = AdminService(db)
    report = admin_service.get_report(report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return report

@router.put("/{report_id}")
async def update_report_status(
    report_id: str,
    status: str,
    db: Session = Depends(get_db)
):
    """Update report status"""
    admin_service = AdminService(db)
    report = admin_service.get_report(report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return admin_service.update_report_status(report_id, status)
