from sqlalchemy.orm import Session
from typing import Optional, List
from passlib.context import CryptContext
from app.db.models import AdminUser, Report, AuditLog
from app.schemas.admin import AdminUserCreate, ReportCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_hash(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    # Admin User Methods
    def create_admin_user(self, user: AdminUserCreate) -> AdminUser:
        db_user = AdminUser(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            role=user.role,
            hashed_password=self.get_hash(user.password)
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_admin_user(self, user_id: str) -> Optional[AdminUser]:
        return self.db.query(AdminUser).filter(AdminUser.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[AdminUser]:
        return self.db.query(AdminUser).filter(AdminUser.email == email).first()
    
    def list_admin_users(self, skip: int = 0, limit: int = 10) -> List[AdminUser]:
        return self.db.query(AdminUser).offset(skip).limit(limit).all()
    
    def delete_admin_user(self, user_id: str) -> None:
        user = self.get_admin_user(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
    
    # Report Methods
    def create_report(self, report: ReportCreate) -> Report:
        db_report = Report(**report.dict())
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        return db_report
    
    def get_report(self, report_id: str) -> Optional[Report]:
        return self.db.query(Report).filter(Report.id == report_id).first()
    
    def list_reports(self, status: str = None, skip: int = 0, limit: int = 20) -> List[Report]:
        query = self.db.query(Report)
        if status:
            query = query.filter(Report.status == status)
        return query.offset(skip).limit(limit).all()
    
    def update_report_status(self, report_id: str, status: str) -> Report:
        report = self.get_report(report_id)
        if report:
            report.status = status
            self.db.commit()
            self.db.refresh(report)
        return report
    
    # Audit Log Methods
    def log_action(self, admin_id: str, action: str, resource_type: str, 
                   resource_id: str, changes: str = None, ip_address: str = None) -> None:
        audit_log = AuditLog(
            admin_id=admin_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            changes=changes,
            ip_address=ip_address
        )
        self.db.add(audit_log)
        self.db.commit()
