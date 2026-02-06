"""Pydantic schemas for audit logging"""

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class AuditLogBase(BaseModel):
    """Base audit log schema"""
    event_type: str = Field(..., description="Type of event")
    session_id: Optional[str] = Field(None, description="Session identifier")
    clinician_id: Optional[str] = Field(None, description="Clinician identifier")
    details: Dict[str, Any] = Field(default_factory=dict, description="Event details")
    ip_address: Optional[str] = Field(None, description="IP address")


class AuditLogCreate(AuditLogBase):
    """Schema for creating an audit log"""
    pass


class AuditLogResponse(AuditLogBase):
    """Schema for audit log response"""
    log_id: str = Field(..., description="Unique log identifier")
    timestamp: datetime = Field(..., description="Event timestamp")

    model_config = {"from_attributes": True}


class AuditLogFilters(BaseModel):
    """Schema for audit log query filters"""
    start_date: Optional[datetime] = Field(None, description="Start date filter")
    end_date: Optional[datetime] = Field(None, description="End date filter")
    session_id: Optional[str] = Field(None, description="Session ID filter")
    clinician_id: Optional[str] = Field(None, description="Clinician ID filter")
    event_type: Optional[str] = Field(None, description="Event type filter")
    limit: int = Field(100, ge=1, le=1000, description="Maximum results")
    offset: int = Field(0, ge=0, description="Results offset")
