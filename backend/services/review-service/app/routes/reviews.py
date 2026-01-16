from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate, ProductReviewStatsResponse
from app.services.review_service import ReviewService
from app.deps.db import get_db

router = APIRouter()

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db)
):
    """Create a new review"""
    if not (1 <= review.rating <= 5):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )
    review_service = ReviewService(db)
    return review_service.create(review)

@router.get("/product/{product_id}", response_model=List[ReviewResponse])
async def get_product_reviews(
    product_id: str,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get all reviews for a product"""
    review_service = ReviewService(db)
    return review_service.get_by_product(product_id, skip=skip, limit=limit)

@router.get("/product/{product_id}/stats", response_model=ProductReviewStatsResponse)
async def get_product_stats(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Get review statistics for a product"""
    review_service = ReviewService(db)
    return review_service.get_product_stats(product_id)

@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(
    review_id: str,
    db: Session = Depends(get_db)
):
    """Get review by ID"""
    review_service = ReviewService(db)
    review = review_service.get(review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    return review

@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: str,
    review_update: ReviewUpdate,
    db: Session = Depends(get_db)
):
    """Update review"""
    review_service = ReviewService(db)
    review = review_service.get(review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    return review_service.update(review_id, review_update)

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: str,
    db: Session = Depends(get_db)
):
    """Delete review"""
    review_service = ReviewService(db)
    review = review_service.get(review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    review_service.delete(review_id)
    return None
