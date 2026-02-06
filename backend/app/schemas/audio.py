"""Pydantic schemas for audio recording"""

from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class AudioRecordingBase(BaseModel):
    """Base audio recording schema"""
    session_id: str = Field(..., description="Unique session identifier")
    clinician_id: str = Field(..., description="Clinician identifier")
    client_id: Optional[str] = Field(None, description="Client identifier")
    duration: int = Field(..., ge=0, description="Recording duration in seconds")
    format: str = Field(..., description="Audio format (wav, mp3, etc.)")
    sample_rate: int = Field(..., ge=8000, description="Sample rate in Hz")


class AudioRecordingCreate(AudioRecordingBase):
    """Schema for creating an audio recording"""
    file_size: int = Field(..., ge=0, description="File size in bytes")
    encrypted_file_path: str = Field(..., description="Path to encrypted audio file")
    encryption_key_id: str = Field(..., description="Encryption key identifier")
    consent_record_id: str = Field(..., description="Associated consent record ID")


class AudioRecordingResponse(AudioRecordingBase):
    """Schema for audio recording response"""
    recording_id: str = Field(..., description="Unique recording identifier")
    recording_date: datetime = Field(..., description="Recording date and time")
    file_size: int = Field(..., description="File size in bytes")
    encrypted_file_path: str = Field(..., description="Path to encrypted audio file")
    encryption_key_id: str = Field(..., description="Encryption key identifier")
    consent_record_id: str = Field(..., description="Associated consent record ID")
    status: Literal["uploaded", "processing", "transcribed", "failed"] = Field(
        ..., description="Processing status"
    )
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Record update timestamp")

    model_config = {"from_attributes": True}


class RecordingSession(BaseModel):
    """Schema for active recording session"""
    session_id: str = Field(..., description="Unique session identifier")
    start_time: datetime = Field(..., description="Recording start time")
    status: Literal["recording", "paused", "stopped"] = Field(
        ..., description="Recording status"
    )
    duration: int = Field(..., ge=0, description="Current duration in seconds")


class RecordingStatus(BaseModel):
    """Schema for recording status query"""
    session_id: str = Field(..., description="Unique session identifier")
    status: Literal["recording", "paused", "stopped", "uploading", "completed"] = Field(
        ..., description="Current status"
    )
    duration: int = Field(..., ge=0, description="Duration in seconds")
    error_message: Optional[str] = Field(None, description="Error message if failed")


class AudioUploadResponse(BaseModel):
    """Schema for audio upload response"""
    recording_id: str = Field(..., description="Unique recording identifier")
    status: str = Field(..., description="Upload status")
    message: str = Field(..., description="Status message")
