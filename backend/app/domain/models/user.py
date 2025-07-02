"""
User domain model for the application.
"""

from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class User:
    """Pure domain model for User"""
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate business rules"""
        if not self.username.strip():
            raise ValueError("Username cannot be empty")
        if len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if len(self.username) > 50:
            raise ValueError("Username cannot exceed 50 characters")
        if not self.email or "@" not in self.email:
            raise ValueError("Valid email is required")
        if len(self.email) > 100:
            raise ValueError("Email cannot exceed 100 characters")
        if self.full_name and len(self.full_name) > 100:
            raise ValueError("Full name cannot exceed 100 characters")

    def deactivate(self) -> None:
        """Deactivate the user"""
        self.is_active = False

    def activate(self) -> None:
        """Activate the user"""
        self.is_active = True

    def promote_to_superuser(self) -> None:
        """Promote user to superuser"""
        self.is_superuser = True

    def demote_from_superuser(self) -> None:
        """Demote user from superuser"""
        self.is_superuser = False

    def update_profile(self, email: Optional[str] = None, full_name: Optional[str] = None) -> None:
        """Update user profile information"""
        if email:
            if "@" not in email:
                raise ValueError("Valid email is required")
            if len(email) > 100:
                raise ValueError("Email cannot exceed 100 characters")
            self.email = email
        
        if full_name is not None:
            if len(full_name) > 100:
                raise ValueError("Full name cannot exceed 100 characters")
            self.full_name = full_name
