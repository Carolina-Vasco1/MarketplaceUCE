from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SalesReportResponse(BaseModel):
    id: str
    seller_id: str
    period: str
    total_sales: float
    total_orders: int
    avg_order_value: float
    total_revenue: float
    commission_paid: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AnalyticsMetric(BaseModel):
    metric_type: str
    value: float
    dimension: Optional[str] = None
    created_at: datetime

class UserReportResponse(BaseModel):
    user_id: str
    total_purchases: int
    total_spent: float
    avg_rating: float
    total_reviews: int
    last_purchase_date: Optional[datetime]
    
    class Config:
        from_attributes = True

class DashboardSummary(BaseModel):
    total_users: int
    total_revenue: float
    total_orders: int
    active_sellers: int
    period: str
