"""SQLAlchemy ORM models for audio recording"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class RecordingStatus(str, enum.Enum):
    """Enum for recording status"""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    TRANSCRIBED = "transcribed"
    FAILED = "failed"


class AudioRecording(Base):
    """ORM model for audio recordings"""
    __tablename__ = "audio_recordings"

    recording_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        comment="Unique recording identifier"
    )
    session_id = Column(
        String(255),
        nullable=False,
        index=True,
        comment="Unique session identifier"
    )
    clinician_id = Column(
        String(255),
        nullable=False,
        index=True,
        comment="Clinician identifier"
    )
    client_id = Column(
        String(255),
        nullable=True,
        index=True,
        comment="Client identifier"
    )
    recording_date = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        comment="Recording date and time"
    )
    duration = Column(
        Integer,
        nullable=False,
        comment="Recording duration in seconds"
    )
    file_size = Column(
        Integer,
        nullable=False,
        comment="File size in bytes"
    )
    encrypted_file_path = Column(
        String(500),
        nullable=False,
        comment="Path to encrypted audio file"
    )
    encryption_key_id = Column(
        String(255),
        nullable=False,
        comment="Encryption key identifier"
    )
    format = Column(
        String(50),
        nullable=False,
        comment="Audio format (wav, mp3, etc.)"
    )
    sample_rate = Column(
        Integer,
        nullable=False,
        comment="Sample rate in Hz"
    )
    consent_record_id = Column(
        UUID(as_uuid=True),
        ForeignKey("consent_records.consent_id"),
        nullable=False,
        comment="Associated consent record ID"
    )
    status = Column(
        Enum(RecordingStatus, name="recording_status_enum"),
        nullable=False,
        default=RecordingStatus.UPLOADED,
        comment="Processing status"
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        comment="Record creation timestamp"
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="Record update timestamp"
    )

    # Relationships
    consent_record = relationship("ConsentRecord", backref="audio_recordings")

    def __repr__(self):
        return f"<AudioRecording(recording_id={self.recording_id}, session_id={self.session_id})>"
