"""FastAPI dependencies for authentication and authorization"""

from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User, UserRole
from app.auth.jwt import verify_token
from app.schemas.user import UserInDB


# HTTP Bearer token security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Bearer credentials containing JWT token
        db: Database session
        
    Returns:
        User object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    # Verify and decode token
    payload = verify_token(token, token_type="access")
    
    # Extract user ID from token
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Fetch user from database
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user (must be active and verified).
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User object
        
    Raises:
        HTTPException: If user is inactive or not verified
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account"
        )
    
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account not verified"
        )
    
    return current_user


def require_role(allowed_roles: List[UserRole]):
    """
    Create a dependency that requires specific user roles (RBAC).
    
    Args:
        allowed_roles: List of allowed user roles
        
    Returns:
        FastAPI dependency function
        
    Example:
        @app.get("/admin")
        async def admin_endpoint(
            user: User = Depends(require_role([UserRole.ADMIN]))
        ):
            return {"message": "Admin access granted"}
    """
    async def role_checker(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        """Check if user has required role"""
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {[r.value for r in allowed_roles]}"
            )
        return current_user
    
    return role_checker


# Convenience dependencies for common role requirements
require_admin = require_role([UserRole.ADMIN])
require_clinician = require_role([UserRole.ADMIN, UserRole.CLINICIAN, UserRole.SUPERVISOR])
require_supervisor = require_role([UserRole.ADMIN, UserRole.SUPERVISOR])


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Get current user if authenticated, otherwise return None.
    Useful for endpoints that have optional authentication.
    
    Args:
        credentials: Optional HTTP Bearer credentials
        db: Database session
        
    Returns:
        User object if authenticated, None otherwise
    """
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        payload = verify_token(token, token_type="access")
        user_id: str = payload.get("sub")
        
        if user_id is None:
            return None
        
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        return user
    except HTTPException:
        return None
