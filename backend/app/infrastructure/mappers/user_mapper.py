"""
Mapper for converting between User domain model and UserEntity persistence model.
"""

from typing import Optional
from datetime import datetime
from app.domain.models.user import User
from app.infrastructure.persistence.user_entity import UserEntity


class UserMapper:
    """Maps between User domain model and UserEntity persistence model"""
    
    @staticmethod
    def to_domain(entity: UserEntity) -> User:
        """Convert UserEntity to User domain model"""
        return User(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            full_name=entity.full_name,
            is_active=entity.is_active,
            is_superuser=entity.is_superuser,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
    
    @staticmethod
    def to_entity(domain: User, hashed_password: str) -> UserEntity:
        """Convert User domain model to UserEntity"""
        return UserEntity(
            id=domain.id,
            username=domain.username,
            email=domain.email,
            hashed_password=hashed_password,
            full_name=domain.full_name,
            is_active=domain.is_active,
            is_superuser=domain.is_superuser,
            created_at=domain.created_at or datetime.now(),
            updated_at=domain.updated_at or datetime.now()
        )
    
    @staticmethod
    def update_entity_from_domain(entity: UserEntity, domain: User) -> UserEntity:
        """Update UserEntity with values from User domain model"""
        entity.username = domain.username
        entity.email = domain.email
        entity.full_name = domain.full_name
        entity.is_active = domain.is_active
        entity.is_superuser = domain.is_superuser
        entity.updated_at = datetime.now()
        return entity
