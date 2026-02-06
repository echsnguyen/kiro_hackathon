"""Authentication service for user management and authentication"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from uuid import UUID
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User, UserRole
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    LoginRequest,
    Token,
    LoginResponse,
    UserResponse,
    OAuthLoginRequest
)
from app.auth.password import hash_password, verify_password
from app.auth.jwt import create_access_token, create_refresh_token, verify_token
from app.auth.oauth import get_oauth_provider
from app.config import settings


class AuthService:
    """Service for authentication and user management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user with hashed password.
        
        Args:
            user_data: User creation data
            
        Returns:
            Created user object
            
        Raises:
            HTTPException: If email already exists
        """
        # Check if user already exists
        result = await self.db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            role=user_data.role,
            hashed_password=hash_password(user_data.password),
            is_active=True,
            is_verified=False,  # Require email verification
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def authenticate_user(self, login_data: LoginRequest) -> User:
        """
        Authenticate user with email and password.
        
        Args:
            login_data: Login credentials
            
        Returns:
            Authenticated user object
            
        Raises:
            HTTPException: If credentials are invalid
        """
        # Find user by email
        result = await self.db.execute(
            select(User).where(User.email == login_data.email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Verify password
        if not user.hashed_password or not verify_password(
            login_data.password, user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Update last login
        user.last_login = datetime.utcnow()
        await self.db.commit()
        
        return user
    
    async def authenticate_oauth(self, oauth_data: OAuthLoginRequest) -> User:
        """
        Authenticate user with OAuth token.
        
        Args:
            oauth_data: OAuth login data
            
        Returns:
            Authenticated user object (created if doesn't exist)
            
        Raises:
            HTTPException: If OAuth token is invalid
        """
        # Get OAuth provider
        provider = get_oauth_provider(oauth_data.provider)
        
        # Verify token and get user info
        token_payload = await provider.verify_token(oauth_data.access_token)
        user_info = await provider.get_user_info(oauth_data.access_token)
        
        # Extract user data
        oauth_subject = token_payload.get("sub")
        email = user_info.get("email")
        name = user_info.get("name") or email.split("@")[0]
        
        if not oauth_subject or not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OAuth token: missing required fields"
            )
        
        # Find or create user
        result = await self.db.execute(
            select(User).where(User.oauth_subject == oauth_subject)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # Check if email already exists
            result = await self.db.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar_one_or_none()
            
            if user:
                # Link existing user to OAuth
                user.oauth_provider = oauth_data.provider
                user.oauth_subject = oauth_subject
                user.is_verified = True  # OAuth users are pre-verified
            else:
                # Create new user
                user = User(
                    email=email,
                    full_name=name,
                    role=UserRole.CLINICIAN,  # Default role
                    oauth_provider=oauth_data.provider,
                    oauth_subject=oauth_subject,
                    is_active=True,
                    is_verified=True,  # OAuth users are pre-verified
                )
                self.db.add(user)
        
        # Update last login
        user.last_login = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    def create_tokens(self, user: User) -> Token:
        """
        Create access and refresh tokens for user.
        
        Args:
            user: User object
            
        Returns:
            Token object with access and refresh tokens
        """
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "token_version": user.refresh_token_version,
        }
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.jwt_access_token_expire_minutes * 60
        )
    
    async def refresh_access_token(self, refresh_token: str) -> Token:
        """
        Refresh access token using refresh token.
        
        Args:
            refresh_token: Refresh token string
            
        Returns:
            New token object
            
        Raises:
            HTTPException: If refresh token is invalid
        """
        # Verify refresh token
        payload = verify_token(refresh_token, token_type="refresh")
        
        user_id = payload.get("sub")
        token_version = payload.get("token_version")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Get user from database
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Verify token version (for token revocation)
        if token_version != user.refresh_token_version:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Create new tokens
        return self.create_tokens(user)
    
    async def logout_user(self, user: User) -> None:
        """
        Logout user by revoking all refresh tokens.
        
        Args:
            user: User object
        """
        # Rotate refresh token version to invalidate all existing tokens
        user.refresh_token_version = str(uuid.uuid4())
        await self.db.commit()
    
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User UUID
            
        Returns:
            User object or None
        """
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> User:
        """
        Update user information.
        
        Args:
            user_id: User UUID
            user_data: User update data
            
        Returns:
            Updated user object
            
        Raises:
            HTTPException: If user not found
        """
        user = await self.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update fields
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
