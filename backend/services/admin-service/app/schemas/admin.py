from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AdminUserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    role: str = "admin"

class AdminUserCreate(AdminUserBase):
    password: str

class AdminUserResponse(AdminUserBase):
    id: str
    is_active: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AuditLogResponse(BaseModel):
    id: str
    admin_id: str
    action: str
    resource_type: str
    resource_id: str
    changes: Optional[str]
    ip_address: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReportCreate(BaseModel):
    reporter_id: str
    reported_user_id: Optional[str] = None
    reported_product_id: Optional[str] = None
    reason: str
    description: Optional[str] = None

class ReportResponse(ReportCreate):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
