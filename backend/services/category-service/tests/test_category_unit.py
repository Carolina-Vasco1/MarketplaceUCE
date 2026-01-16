import pytest
from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate
from app.services.category_service import CategoryService

@pytest.fixture
def category_service(db: Session):
    return CategoryService(db)

def test_create_category(category_service):
    """Test creating a new category"""
    category_data = CategoryCreate(
        name="Electronics",
        slug="electronics"
    )
    category = category_service.create(category_data)
    assert category.name == "Electronics"
    assert category.slug == "electronics"

def test_get_category(category_service):
    """Test retrieving a category"""
    category_data = CategoryCreate(name="Books", slug="books")
    created = category_service.create(category_data)
    retrieved = category_service.get(created.id)
    assert retrieved.id == created.id
