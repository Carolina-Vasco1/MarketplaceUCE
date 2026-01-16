from sqlalchemy import Column, String, DateTime, Integer, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class SalesReport(Base):
    __tablename__ = "sales_reports"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    seller_id = Column(String, nullable=False, index=True)
    period = Column(String, nullable=False)  # daily, weekly, monthly
    total_sales = Column(Float, default=0)
    total_orders = Column(Integer, default=0)
    avg_order_value = Column(Float, default=0)
    total_revenue = Column(Float, default=0)
    commission_paid = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AnalyticsData(Base):
    __tablename__ = "analytics_data"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    metric_type = Column(String, nullable=False)  # user_growth, sales, traffic, etc
    value = Column(Float, nullable=False)
    dimension = Column(String, nullable=True)  # hourly, daily, weekly, monthly
    metadata = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserReport(Base):
    __tablename__ = "user_reports"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    total_purchases = Column(Integer, default=0)
    total_spent = Column(Float, default=0)
    avg_rating = Column(Float, default=0)
    total_reviews = Column(Integer, default=0)
    last_purchase_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
