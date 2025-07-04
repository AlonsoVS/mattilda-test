"""
User repository implementation for infrastructure layer.
"""

from typing import Optional, List
from sqlmodel import Session, select
from datetime import datetime
from app.domain.repositories.user_repository import UserRepositoryInterface
from app.domain.models.user import User
from app.infrastructure.persistence.user_entity import UserEntity
from app.infrastructure.mappers.user_mapper import UserMapper


class UserRepository(UserRepositoryInterface):
    """SQLModel implementation of user repository."""
    
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, user: User, hashed_password: str) -> User:
        """Create a new user."""
        user_entity = UserMapper.to_entity(user, hashed_password)
        
        self.session.add(user_entity)
        self.session.commit()
        self.session.refresh(user_entity)
        
        return UserMapper.to_domain(user_entity)
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        statement = select(UserEntity).where(UserEntity.id == user_id)
        result = self.session.exec(statement).first()
        return UserMapper.to_domain(result) if result else None
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        statement = select(UserEntity).where(UserEntity.username == username)
        result = self.session.exec(statement).first()
        return UserMapper.to_domain(result) if result else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        statement = select(UserEntity).where(UserEntity.email == email)
        result = self.session.exec(statement).first()
        return UserMapper.to_domain(result) if result else None
    
    async def list_all(self) -> List[User]:
        """Get all users."""
        statement = select(UserEntity)
        results = self.session.exec(statement).all()
        return [UserMapper.to_domain(entity) for entity in results]
    
    async def update(self, user_id: int, updates: dict) -> Optional[User]:
        """Update user information."""
        statement = select(UserEntity).where(UserEntity.id == user_id)
        user_entity = self.session.exec(statement).first()
        
        if not user_entity:
            return None
        
        # Update fields
        for field, value in updates.items():
            if hasattr(user_entity, field) and value is not None:
                setattr(user_entity, field, value)
        
        user_entity.updated_at = datetime.now()
        self.session.commit()
        self.session.refresh(user_entity)
        
        return UserMapper.to_domain(user_entity)
    
    async def delete(self, user_id: int) -> bool:
        """Delete user."""
        statement = select(UserEntity).where(UserEntity.id == user_id)
        user_entity = self.session.exec(statement).first()
        
        if not user_entity:
            return False
        
        self.session.delete(user_entity)
        self.session.commit()
        return True
    
    async def get_hashed_password(self, username: str) -> Optional[str]:
        """Get user's hashed password for authentication."""
        statement = select(UserEntity.hashed_password).where(UserEntity.username == username)
        result = self.session.exec(statement).first()
        return result
    
    async def update_password(self, user_id: int, hashed_password: str) -> bool:
        """Update user's password."""
        statement = select(UserEntity).where(UserEntity.id == user_id)
        user_entity = self.session.exec(statement).first()
        
        if not user_entity:
            return False
        
        user_entity.hashed_password = hashed_password
        user_entity.updated_at = datetime.now()
        self.session.commit()
        return True
