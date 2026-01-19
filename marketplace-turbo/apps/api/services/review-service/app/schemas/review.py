from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    product_id: str
    user_id: str
    seller_id: str
    rating: int  # 1-5
    title: str
    comment: Optional[str] = None
    is_verified_purchase: int = 0

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    title: Optional[str] = None
    comment: Optional[str] = None

class ReviewResponse(ReviewBase):
    id: str
    helpful_count: int
    unhelpful_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProductReviewStatsResponse(BaseModel):
    product_id: str
    average_rating: float
    total_reviews: int
    ratings_distribution: dict  # {1: count, 2: count, etc}
