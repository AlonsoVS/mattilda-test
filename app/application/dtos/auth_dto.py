"""
Authentication Data Transfer Objects (DTOs) for API requests and responses.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserLoginDTO(BaseModel):
    """DTO for user login request."""
    username: str
    password: str


class UserCreateDTO(BaseModel):
    """DTO for user registration request."""
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserResponseDTO(BaseModel):
    """DTO for user data in responses."""
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    is_superuser: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TokenResponseDTO(BaseModel):
    """DTO for authentication token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes in seconds


class TokenRefreshDTO(BaseModel):
    """DTO for token refresh request."""
    refresh_token: str


class UserUpdateDTO(BaseModel):
    """DTO for user profile update."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class ChangePasswordDTO(BaseModel):
    """DTO for password change request."""
    current_password: str
    new_password: str
