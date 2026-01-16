import pytest
from sqlalchemy.orm import Session
from app.services.reporting_service import ReportingService

@pytest.fixture
def reporting_service(db: Session):
    return ReportingService(db)

def test_get_sales_summary(reporting_service):
    """Test getting sales summary"""
    summary = reporting_service.get_sales_summary("seller1")
    assert "seller_id" in summary
    assert "total_sales" in summary

def test_get_platform_summary(reporting_service):
    """Test getting platform summary"""
    summary = reporting_service.get_platform_summary()
    assert "total_sales" in summary
    assert "total_orders" in summary
