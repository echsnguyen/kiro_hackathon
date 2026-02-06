"""Pydantic schemas for consent management"""

from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class ConsentRecordBase(BaseModel):
    """Base consent record schema"""
    session_id: str = Field(..., description="Unique session identifier")
    clinician_id: str = Field(..., description="Clinician identifier")
    client_id: Optional[str] = Field(None, description="Client identifier")
    consent_method: Literal["digital_signature", "verbal_timestamp"] = Field(
        ..., description="Method of consent collection"
    )
    signature_data: Optional[str] = Field(None, description="Digital signature data")


class ConsentRecordCreate(ConsentRecordBase):
    """Schema for creating a consent record"""
    ip_address: str = Field(..., description="IP address of the request")
    device_info: str = Field(..., description="Device information")


class ConsentRecordResponse(ConsentRecordBase):
    """Schema for consent record response"""
    consent_id: str = Field(..., description="Unique consent identifier")
    timestamp: datetime = Field(..., description="Timestamp of consent")
    encrypted_signature_path: Optional[str] = Field(
        None, description="Path to encrypted signature file"
    )
    created_at: datetime = Field(..., description="Record creation timestamp")

    model_config = {"from_attributes": True}
