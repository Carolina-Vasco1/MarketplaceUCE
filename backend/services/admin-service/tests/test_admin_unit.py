import pytest
from sqlalchemy.orm import Session
from app.schemas.admin import AdminUserCreate, ReportCreate
from app.services.admin_service import AdminService

@pytest.fixture
def admin_service(db: Session):
    return AdminService(db)

def test_create_admin_user(admin_service):
    """Test creating admin user"""
    user_data = AdminUserCreate(
        email="admin@test.com",
        username="admin",
        password="secure_password",
        role="admin"
    )
    user = admin_service.create_admin_user(user_data)
    assert user.email == "admin@test.com"
    assert user.role == "admin"

def test_create_report(admin_service):
    """Test creating report"""
    report_data = ReportCreate(
        reporter_id="user1",
        reported_product_id="prod1",
        reason="Inappropriate content"
    )
    report = admin_service.create_report(report_data)
    assert report.status == "pending"
