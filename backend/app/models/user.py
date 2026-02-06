"""User database model"""

from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from app.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration for RBAC"""
    ADMIN = "admin"
    CLINICIAN = "clinician"
    SUPERVISOR = "supervisor"
    VIEWER = "viewer"


class User(Base):
    """User model for authentication and authorization"""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=True)  # Nullable for OAuth-only users
    full_name = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.CLINICIAN)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # OAuth fields
    oauth_provider = Column(String(50), nullable=True)  # 'auth0', 'cognito', etc.
    oauth_subject = Column(String(255), nullable=True, unique=True, index=True)
    
    # Session management
    last_login = Column(DateTime, nullable=True)
    refresh_token_version = Column(String(36), default=lambda: str(uuid.uuid4()))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
