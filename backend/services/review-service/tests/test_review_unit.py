import pytest
from sqlalchemy.orm import Session
from app.schemas.review import ReviewCreate
from app.services.review_service import ReviewService

@pytest.fixture
def review_service(db: Session):
    return ReviewService(db)

def test_create_review(review_service):
    """Test creating a review"""
    review_data = ReviewCreate(
        product_id="prod1",
        user_id="user1",
        seller_id="seller1",
        rating=5,
        title="Great product!"
    )
    review = review_service.create(review_data)
    assert review.rating == 5
    assert review.title == "Great product!"

def test_get_product_reviews(review_service):
    """Test getting reviews for a product"""
    review_data = ReviewCreate(
        product_id="prod1",
        user_id="user1",
        seller_id="seller1",
        rating=4,
        title="Good"
    )
    review_service.create(review_data)
    reviews = review_service.get_by_product("prod1")
    assert len(reviews) > 0
