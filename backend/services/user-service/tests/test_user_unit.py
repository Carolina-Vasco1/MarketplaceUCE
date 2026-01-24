import pytest
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.services.user_service import UserService

@pytest.fixture
def user_service(db: Session):
    return UserService(db)

def test_create_user(user_service):
    """Test creating a new user"""
    user_data = UserCreate(
        email="test@example.com",
        full_name="Test User",
        phone="+1234567890"
    )
    user = user_service.create(user_data)
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"

def test_get_user(user_service):
    """Test retrieving a user"""
    user_data = UserCreate(email="test@example.com")
    created_user = user_service.create(user_data)
    retrieved_user = user_service.get(created_user.id)
    assert retrieved_user.id == created_user.id
