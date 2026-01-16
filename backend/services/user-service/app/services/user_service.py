from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user: UserCreate) -> User:
        """Create a new user"""
        db_user = User(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def list(self, skip: int = 0, limit: int = 10) -> List[User]:
        """Get list of users with pagination"""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def update(self, user_id: str, user_update: UserUpdate) -> User:
        """Update user information"""
        db_user = self.get(user_id)
        if db_user:
            update_data = user_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user
    
    def delete(self, user_id: str) -> None:
        """Delete a user"""
        db_user = self.get(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
