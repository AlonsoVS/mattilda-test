"""
Authentication service for handling user authentication operations.
"""

from datetime import timedelta
from typing import Optional, List
from fastapi import HTTPException, status
from app.domain.repositories.user_repository import UserRepositoryInterface
from app.domain.models.user import User
from app.application.dtos.auth_dto import UserCreateDTO, UserLoginDTO, UserUpdateDTO, ChangePasswordDTO
from app.core.config import settings
from app.core.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    create_refresh_token,
    verify_refresh_token
)

class AuthService:
    """Service for user authentication operations."""
    
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository
    
    async def register_user(self, user_data: UserCreateDTO) -> User:
        """Register a new user."""
        # Check if username already exists
        existing_user = await self.user_repository.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        existing_email = await self.user_repository.get_by_email(user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        hashed_password = get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            is_active=True,
            is_superuser=False
        )
        
        return await self.user_repository.create(user, hashed_password)
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user by username and password."""
        user = await self.user_repository.get_by_username(username)
        if not user:
            return None
        
        if not user.is_active:
            return None
        
        hashed_password = await self.user_repository.get_hashed_password(username)
        if not hashed_password or not verify_password(password, hashed_password):
            return None
        
        return user
    
    async def login(self, login_data: UserLoginDTO) -> dict:
        """Login user and return tokens."""
        user = await self.authenticate_user(login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create tokens with environment-configured expiration
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id}, 
            expires_delta=expires_delta
        )
        refresh_token = create_refresh_token(data={"sub": user.username, "user_id": user.id})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert minutes to seconds
        }
    
    async def refresh_token(self, refresh_token: str) -> dict:
        """Refresh access token using refresh token."""
        payload = verify_refresh_token(refresh_token)
        username = payload.get("sub")
        user_id = payload.get("user_id")
        
        if not username or not isinstance(username, str):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Verify user still exists and is active
        user = await self.user_repository.get_by_username(username)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new tokens with environment-configured expiration
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username, "user_id": user_id}, 
            expires_delta=expires_delta
        )
        new_refresh_token = create_refresh_token(data={"sub": username, "user_id": user_id})
        
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert minutes to seconds
        }
    
    async def get_current_user(self, username: str) -> Optional[User]:
        """Get current user by username from token."""
        user = await self.user_repository.get_by_username(username)
        if not user or not user.is_active:
            return None
        return user
    
    async def update_user_profile(self, user_id: int, update_data: UserUpdateDTO) -> Optional[User]:
        """Update user profile information."""
        # Check if email is being changed and if it's already taken
        if update_data.email:
            existing_user = await self.user_repository.get_by_email(update_data.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        updates = {}
        if update_data.email is not None:
            updates["email"] = update_data.email
        if update_data.full_name is not None:
            updates["full_name"] = update_data.full_name
        if update_data.is_active is not None:
            updates["is_active"] = update_data.is_active
        
        return await self.user_repository.update(user_id, updates)
    
    async def change_password(self, user_id: int, password_data: ChangePasswordDTO) -> bool:
        """Change user password."""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify current password
        hashed_password = await self.user_repository.get_hashed_password(user.username)
        if not hashed_password or not verify_password(password_data.current_password, hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Update password
        new_hashed_password = get_password_hash(password_data.new_password)
        return await self.user_repository.update_password(user_id, new_hashed_password)
    
    async def list_users(self) -> List[User]:
        """Get all users (admin only)."""
        return await self.user_repository.list_all()
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID (admin only)."""
        return await self.user_repository.get_by_id(user_id)
