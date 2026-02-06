"""SQLAlchemy ORM models for portal submission"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class SubmissionStatus(str, enum.Enum):
    """Enum for submission status"""
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"
    RETRYING = "retrying"


class SubmissionRecord(Base):
    """ORM model for submission records"""
    __tablename__ = "submission_records"

    submission_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        comment="Unique submission identifier"
    )
    session_id = Column(
        String(255),
        nullable=False,
        index=True,
        comment="Session identifier"
    )
    clinical_data_id = Column(
        UUID(as_uuid=True),
        ForeignKey("clinical_data_records.clinical_data_id"),
        nullable=False,
        index=True,
        comment="Clinical data identifier"
    )
    clinician_id = Column(
        String(255),
        nullable=False,
        index=True,
        comment="Clinician identifier"
    )
    submission_date = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        comment="Submission date"
    )
    status = Column(
        Enum(SubmissionStatus, name="submission_status_enum"),
        nullable=False,
        default=SubmissionStatus.PENDING,
        comment="Submission status"
    )
    portal_record_id = Column(
        String(255),
        nullable=True,
        index=True,
        comment="Portal record identifier"
    )
    error_message = Column(
        Text,
        nullable=True,
        comment="Error message if failed"
    )
    retry_count = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Number of retry attempts"
    )
    last_retry_at = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Last retry timestamp"
    )
    payload = Column(
        Text,
        nullable=False,
        comment="JSON payload submitted to portal (encrypted)"
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
    clinical_data_record = relationship("ClinicalDataRecord", backref="submission_records")

    def __repr__(self):
        return f"<SubmissionRecord(submission_id={self.submission_id}, session_id={self.session_id})>"
