from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from app.db.models import Review
from app.schemas.review import ReviewCreate, ReviewUpdate

class ReviewService:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, review: ReviewCreate) -> Review:
        """Create a new review"""
        db_review = Review(**review.dict())
        self.db.add(db_review)
        self.db.commit()
        self.db.refresh(db_review)
        return db_review
    
    def get(self, review_id: str) -> Optional[Review]:
        """Get review by ID"""
        return self.db.query(Review).filter(Review.id == review_id).first()
    
    def get_by_product(self, product_id: str, skip: int = 0, limit: int = 20) -> List[Review]:
        """Get reviews for a product"""
        return self.db.query(Review).filter(
            Review.product_id == product_id
        ).offset(skip).limit(limit).all()
    
    def get_product_stats(self, product_id: str):
        """Get review statistics for a product"""
        reviews = self.db.query(Review).filter(Review.product_id == product_id).all()
        
        if not reviews:
            return {
                "product_id": product_id,
                "average_rating": 0,
                "total_reviews": 0,
                "ratings_distribution": {}
            }
        
        ratings_dist = {i: 0 for i in range(1, 6)}
        total_rating = 0
        
        for review in reviews:
            ratings_dist[review.rating] += 1
            total_rating += review.rating
        
        return {
            "product_id": product_id,
            "average_rating": round(total_rating / len(reviews), 2),
            "total_reviews": len(reviews),
            "ratings_distribution": ratings_dist
        }
    
    def update(self, review_id: str, review_update: ReviewUpdate) -> Review:
        """Update review"""
        db_review = self.get(review_id)
        if db_review:
            update_data = review_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_review, key, value)
            self.db.commit()
            self.db.refresh(db_review)
        return db_review
    
    def delete(self, review_id: str) -> None:
        """Delete review"""
        db_review = self.get(review_id)
        if db_review:
            self.db.delete(db_review)
            self.db.commit()
