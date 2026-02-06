"""SQLAlchemy ORM models for transcription"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class TranscriptStatus(str, enum.Enum):
    """Enum for transcript status"""
    COMPLETED = "completed"
    FAILED = "failed"


class Transcript(Base):
    """ORM model for transcripts"""
    __tablename__ = "transcripts"

    transcript_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        comment="Unique transcript identifier"
    )
    recording_id = Column(
        UUID(as_uuid=True),
        ForeignKey("audio_recordings.recording_id"),
        nullable=False,
        index=True,
        comment="Associated recording ID"
    )
    session_id = Column(
        String(255),
        nullable=False,
        index=True,
        comment="Session identifier"
    )
    raw_text = Column(
        Text,
        nullable=False,
        comment="Full transcript text (encrypted)"
    )
    segments = Column(
        JSONB,
        nullable=False,
        default=list,
        comment="Transcript segments with diarization (encrypted)"
    )
    speakers = Column(
        JSONB,
        nullable=False,
        default=list,
        comment="Identified speakers (encrypted)"
    )
    overall_confidence = Column(
        Float,
        nullable=False,
        comment="Overall transcription confidence"
    )
    processing_time = Column(
        Integer,
        nullable=False,
        comment="Processing time in seconds"
    )
    stt_engine = Column(
        String(100),
        nullable=False,
        comment="STT engine used"
    )
    stt_model_version = Column(
        String(100),
        nullable=False,
        comment="STT model version"
    )
    diarization_confidence = Column(
        Float,
        nullable=False,
        comment="Diarization confidence score"
    )
    status = Column(
        Enum(TranscriptStatus, name="transcript_status_enum"),
        nullable=False,
        default=TranscriptStatus.COMPLETED,
        comment="Processing status"
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        comment="Record creation timestamp"
    )

    # Relationships
    audio_recording = relationship("AudioRecording", backref="transcripts")

    def __repr__(self):
        return f"<Transcript(transcript_id={self.transcript_id}, session_id={self.session_id})>"
