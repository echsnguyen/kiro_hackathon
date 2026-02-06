"""User Pydantic schemas for API validation"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole


class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    role: UserRole = UserRole.CLINICIAN


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    """Schema for user as stored in database"""
    id: UUID
    is_active: bool
    is_verified: bool
    oauth_provider: Optional[str] = None
    oauth_subject: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class UserResponse(BaseModel):
    """Schema for user response (public fields only)"""
    id: UUID
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    
    model_config = {"from_attributes": True}


class TokenPayload(BaseModel):
    """Schema for JWT token payload"""
    sub: str  # User ID
    email: str
    role: UserRole
    exp: int
    iat: int
    type: str  # 'access' or 'refresh'


class Token(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenRefresh(BaseModel):
    """Schema for token refresh request"""
    refresh_token: str


class LoginRequest(BaseModel):
    """Schema for login request"""
    email: EmailStr
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    """Schema for login response"""
    user: UserResponse
    token: Token


class OAuthLoginRequest(BaseModel):
    """Schema for OAuth login request"""
    provider: str = Field(..., pattern="^(auth0|cognito)$")
    access_token: str
