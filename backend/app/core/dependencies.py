"""
Authentication dependencies for FastAPI dependency injection.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from typing import Optional
from app.infrastructure.database.connection import get_session
from app.infrastructure.repositories.user_repository import UserRepository
from app.application.services.auth_service import AuthService
from app.domain.models.user import User
from app.core.auth import verify_token

# HTTP Bearer token scheme
security = HTTPBearer()


def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    """Dependency to get user repository."""
    return UserRepository(session)


def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    """Dependency to get authentication service."""
    return AuthService(user_repository)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """
    Dependency to get current authenticated user.
    
    Args:
        credentials: HTTP Bearer token from request header
        auth_service: Authentication service instance
        
    Returns:
        Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify token and extract payload
        payload = verify_token(credentials.credentials)
        username = payload.get("sub")
        
        if username is None or not isinstance(username, str):
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    # Get user from database
    user = await auth_service.get_current_user(username)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get current active user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current active user
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Dependency to get current superuser.
    
    Args:
        current_user: Current active user
        
    Returns:
        Current superuser
        
    Raises:
        HTTPException: If user is not a superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


# Optional authentication (for endpoints that work with or without auth)
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> Optional[User]:
    """
    Optional dependency to get current user if token is provided.
    
    Args:
        credentials: Optional HTTP Bearer token from request header
        auth_service: Authentication service instance
        
    Returns:
        Current user if authenticated, None otherwise
    """
    if not credentials:
        return None
    
    try:
        payload = verify_token(credentials.credentials)
        username = payload.get("sub")
        
        if username is None or not isinstance(username, str):
            return None
        
        return await auth_service.get_current_user(username)
    except Exception:
        return None
