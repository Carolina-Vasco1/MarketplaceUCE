from sqlalchemy import Column, String, DateTime, Integer, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    seller_id = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    title = Column(String, nullable=False)
    comment = Column(Text, nullable=True)
    helpful_count = Column(Integer, default=0)
    unhelpful_count = Column(Integer, default=0)
    is_verified_purchase = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Review {self.id} - {self.rating}★>"
