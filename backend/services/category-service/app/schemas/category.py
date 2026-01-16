from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    icon_url: Optional[str] = None
    image_url: Optional[str] = None
    parent_id: Optional[str] = None
    display_order: int = 0

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon_url: Optional[str] = None
    image_url: Optional[str] = None
    display_order: Optional[int] = None

class CategoryResponse(CategoryBase):
    id: str
    is_active: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CategoryTreeResponse(CategoryResponse):
    subcategories: List["CategoryResponse"] = []
