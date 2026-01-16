from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

class CategoryService:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, category: CategoryCreate) -> Category:
        """Create a new category"""
        db_category = Category(**category.dict())
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category
    
    def get(self, category_id: str) -> Optional[Category]:
        """Get category by ID"""
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def get_by_slug(self, slug: str) -> Optional[Category]:
        """Get category by slug"""
        return self.db.query(Category).filter(Category.slug == slug).first()
    
    def list(self, skip: int = 0, limit: int = 50) -> List[Category]:
        """Get list of categories"""
        return self.db.query(Category).filter(Category.is_active == 1).offset(skip).limit(limit).all()
    
    def get_tree(self) -> List[Category]:
        """Get categories in tree structure (only parent categories)"""
        return self.db.query(Category).filter(
            Category.parent_id == None,
            Category.is_active == 1
        ).order_by(Category.display_order).all()
    
    def update(self, category_id: str, category_update: CategoryUpdate) -> Category:
        """Update category"""
        db_category = self.get(category_id)
        if db_category:
            update_data = category_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_category, key, value)
            self.db.commit()
            self.db.refresh(db_category)
        return db_category
    
    def delete(self, category_id: str) -> None:
        """Delete category"""
        db_category = self.get(category_id)
        if db_category:
            self.db.delete(db_category)
            self.db.commit()
