"""Pydantic schemas for transcription"""

from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class TranscriptSegment(BaseModel):
    """Schema for a transcript segment"""
    text: str = Field(..., description="Segment text")
    start_time: float = Field(..., ge=0, description="Start time in seconds")
    end_time: float = Field(..., ge=0, description="End time in seconds")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score")
    speaker: Optional[str] = Field(None, description="Speaker identifier")


class Speaker(BaseModel):
    """Schema for a speaker"""
    speaker_id: str = Field(..., description="Unique speaker identifier")
    role: Optional[Literal["clinician", "client", "carer", "unknown"]] = Field(
        None, description="Speaker role"
    )
    segment_count: int = Field(0, ge=0, description="Number of segments")


class DiarizedSegment(TranscriptSegment):
    """Schema for a diarized transcript segment"""
    speaker_id: str = Field(..., description="Speaker identifier")
    speaker_role: Optional[Literal["clinician", "client", "carer", "unknown"]] = Field(
        None, description="Speaker role"
    )


class TranscriptBase(BaseModel):
    """Base transcript schema"""
    recording_id: str = Field(..., description="Associated recording ID")
    session_id: str = Field(..., description="Session identifier")


class TranscriptCreate(TranscriptBase):
    """Schema for creating a transcript"""
    raw_text: str = Field(..., description="Full transcript text")
    segments: List[DiarizedSegment] = Field(
        default_factory=list, description="Transcript segments"
    )
    speakers: List[Speaker] = Field(default_factory=list, description="Speakers")
    overall_confidence: float = Field(..., ge=0, le=1, description="Overall confidence")
    processing_time: int = Field(..., ge=0, description="Processing time in seconds")
    stt_engine: str = Field(..., description="STT engine used")
    stt_model_version: str = Field(..., description="STT model version")
    diarization_confidence: float = Field(
        ..., ge=0, le=1, description="Diarization confidence"
    )


class TranscriptResponse(TranscriptBase):
    """Schema for transcript response"""
    transcript_id: str = Field(..., description="Unique transcript identifier")
    raw_text: str = Field(..., description="Full transcript text")
    segments: List[DiarizedSegment] = Field(..., description="Transcript segments")
    speakers: List[Speaker] = Field(..., description="Speakers")
    overall_confidence: float = Field(..., description="Overall confidence")
    processing_time: int = Field(..., description="Processing time in seconds")
    stt_engine: str = Field(..., description="STT engine used")
    stt_model_version: str = Field(..., description="STT model version")
    diarization_confidence: float = Field(..., description="Diarization confidence")
    status: Literal["completed", "failed"] = Field(..., description="Processing status")
    created_at: datetime = Field(..., description="Record creation timestamp")

    model_config = {"from_attributes": True}


class TranscriptionOptions(BaseModel):
    """Schema for transcription options"""
    language: str = Field("en", description="Language code")
    medical_vocabulary: bool = Field(True, description="Enable medical vocabulary")
    enable_diarization: bool = Field(True, description="Enable speaker diarization")
    streaming_mode: bool = Field(False, description="Enable streaming mode")


class TranscriptionJob(BaseModel):
    """Schema for transcription job"""
    job_id: str = Field(..., description="Unique job identifier")
    status: Literal["queued", "processing", "completed", "failed"] = Field(
        ..., description="Job status"
    )
    message: str = Field(..., description="Status message")


class TranscriptionStatus(BaseModel):
    """Schema for transcription status"""
    job_id: str = Field(..., description="Job identifier")
    status: Literal["queued", "processing", "completed", "failed"] = Field(
        ..., description="Job status"
    )
    progress: int = Field(..., ge=0, le=100, description="Progress percentage")
    error_message: Optional[str] = Field(None, description="Error message if failed")


class DiarizedTranscript(BaseModel):
    """Schema for diarized transcript"""
    job_id: str = Field(..., description="Job identifier")
    segments: List[DiarizedSegment] = Field(..., description="Diarized segments")
    speakers: List[Speaker] = Field(..., description="Identified speakers")
    confidence: float = Field(..., ge=0, le=1, description="Diarization confidence")


class SpeakerRoleMapping(BaseModel):
    """Schema for speaker role mapping"""
    speaker_id: str = Field(..., description="Speaker identifier")
    role: Literal["clinician", "client", "carer"] = Field(..., description="Speaker role")
