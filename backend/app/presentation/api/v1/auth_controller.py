"""
Authentication controller for handling auth-related API endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from app.application.services.auth_service import AuthService
from app.application.dtos.auth_dto import (
    UserLoginDTO, 
    UserCreateDTO, 
    TokenResponseDTO, 
    TokenRefreshDTO,
    UserResponseDTO,
    UserUpdateDTO,
    ChangePasswordDTO
)
from app.domain.models.user import User
from app.core.dependencies import get_auth_service, get_current_active_user, get_current_superuser

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreateDTO,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Register a new user."""
    try:
        user = await auth_service.register_user(user_data)
        return UserResponseDTO.from_orm(user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


@router.post("/login", response_model=TokenResponseDTO)
async def login(
    login_data: UserLoginDTO,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Authenticate user and return access token."""
    try:
        tokens = await auth_service.login(login_data)
        return TokenResponseDTO(**tokens)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during login: {str(e)}"
        )


@router.post("/refresh", response_model=TokenResponseDTO)
async def refresh_token(
    refresh_data: TokenRefreshDTO,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Refresh access token using refresh token."""
    try:
        tokens = await auth_service.refresh_token(refresh_data.refresh_token)
        return TokenResponseDTO(**tokens)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error refreshing token: {str(e)}"
        )


@router.get("/me", response_model=UserResponseDTO)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user profile."""
    return UserResponseDTO.from_orm(current_user)


@router.put("/me", response_model=UserResponseDTO)
async def update_profile(
    update_data: UserUpdateDTO,
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Update current user profile."""
    try:
        if current_user.id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID not found"
            )
        updated_user = await auth_service.update_user_profile(current_user.id, update_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponseDTO.from_orm(updated_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating profile: {str(e)}"
        )


@router.post("/change-password")
async def change_password(
    password_data: ChangePasswordDTO,
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Change current user password."""
    try:
        if current_user.id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID not found"
            )
        success = await auth_service.change_password(current_user.id, password_data)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to change password"
            )
        return {"message": "Password changed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error changing password: {str(e)}"
        )


# Admin endpoints
@router.get("/users", response_model=list[UserResponseDTO])
async def list_users(
    current_user: User = Depends(get_current_superuser),
    auth_service: AuthService = Depends(get_auth_service)
):
    """List all users (admin only)."""
    users = await auth_service.list_users()
    return [UserResponseDTO.model_validate(user) for user in users]


@router.get("/users/{user_id}", response_model=UserResponseDTO)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Get user by ID (admin only)."""
    user = await auth_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponseDTO.model_validate(user)
