"""Authentication API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse,
    LoginRequest,
    LoginResponse,
    Token,
    TokenRefresh,
    OAuthLoginRequest,
)
from app.models.user import User
from app.services.auth_service import AuthService
from app.auth.dependencies import get_current_active_user


router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account.
    
    - **email**: Valid email address
    - **password**: Password (minimum 8 characters)
    - **full_name**: User's full name
    - **role**: User role (default: clinician)
    """
    auth_service = AuthService(db)
    user = await auth_service.create_user(user_data)
    return user


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password.
    
    Returns access token and refresh token.
    """
    auth_service = AuthService(db)
    
    # Authenticate user
    user = await auth_service.authenticate_user(login_data)
    
    # Create tokens
    token = auth_service.create_tokens(user)
    
    return LoginResponse(
        user=UserResponse.model_validate(user),
        token=token
    )


@router.post("/login/oauth", response_model=LoginResponse)
async def login_oauth(
    oauth_data: OAuthLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with OAuth provider (Auth0 or AWS Cognito).
    
    - **provider**: OAuth provider name ('auth0' or 'cognito')
    - **access_token**: OAuth access token from provider
    
    Creates a new user account if one doesn't exist.
    """
    auth_service = AuthService(db)
    
    # Authenticate with OAuth
    user = await auth_service.authenticate_oauth(oauth_data)
    
    # Create tokens
    token = auth_service.create_tokens(user)
    
    return LoginResponse(
        user=UserResponse.model_validate(user),
        token=token
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    
    - **refresh_token**: Valid refresh token
    
    Returns new access token and refresh token.
    """
    auth_service = AuthService(db)
    token = await auth_service.refresh_access_token(token_data.refresh_token)
    return token


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Logout current user.
    
    Revokes all refresh tokens for the user.
    Requires authentication.
    """
    auth_service = AuthService(db)
    await auth_service.logout_user(current_user)
    return None


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current authenticated user information.
    
    Requires authentication.
    """
    return current_user


@router.get("/verify-token")
async def verify_token_endpoint(
    current_user: User = Depends(get_current_active_user)
):
    """
    Verify if the provided token is valid.
    
    Returns user information if token is valid.
    Requires authentication.
    """
    return {
        "valid": True,
        "user": UserResponse.model_validate(current_user)
    }
