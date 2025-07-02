"""
User repository interface for domain layer.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.models.user import User


class UserRepositoryInterface(ABC):
    """Interface for user repository operations."""
    
    @abstractmethod
    async def create(self, user: User, hashed_password: str) -> User:
        """Create a new user."""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[User]:
        """Get all users."""
        pass
    
    @abstractmethod
    async def update(self, user_id: int, updates: dict) -> Optional[User]:
        """Update user information."""
        pass
    
    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """Delete user."""
        pass
    
    @abstractmethod
    async def get_hashed_password(self, username: str) -> Optional[str]:
        """Get user's hashed password for authentication."""
        pass
    
    @abstractmethod
    async def update_password(self, user_id: int, hashed_password: str) -> bool:
        """Update user's password."""
        pass
