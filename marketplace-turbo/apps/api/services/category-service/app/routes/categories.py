from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import re

from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate, CategoryTreeResponse
from app.services.category_service import CategoryService
from app.deps.db import get_db

router = APIRouter()

def slugify(text: str) -> str:
    """Convert text to slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new category"""
    category_service = CategoryService(db)
    
    # Auto-generate slug if not provided
    if not category.slug:
        category.slug = slugify(category.name)
    
    existing = category_service.get_by_slug(category.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category slug already exists"
        )
    return category_service.create(category)

@router.get("/", response_model=List[CategoryResponse])
async def list_categories(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all categories"""
    category_service = CategoryService(db)
    return category_service.list(skip=skip, limit=limit)

@router.get("/tree", response_model=List[CategoryTreeResponse])
async def get_category_tree(db: Session = Depends(get_db)):
    """Get categories in tree structure"""
    category_service = CategoryService(db)
    return category_service.get_tree()

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: str,
    db: Session = Depends(get_db)
):
    """Get category by ID"""
    category_service = CategoryService(db)
    category = category_service.get(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: str,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """Update category"""
    category_service = CategoryService(db)
    category = category_service.get(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category_service.update(category_id, category_update)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str,
    db: Session = Depends(get_db)
):
    """Delete category"""
    category_service = CategoryService(db)
    category = category_service.get(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    category_service.delete(category_id)
    return None
