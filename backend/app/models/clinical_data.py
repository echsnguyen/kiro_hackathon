"""SQLAlchemy ORM models for clinical data"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class ClinicalDataStatus(str, enum.Enum):
    """Enum for clinical data status"""
    DRAFT = "draft"
    VALIDATED = "validated"
    SUBMITTED = "submitted"


class ClinicalDataRecord(Base):
    """ORM model for clinical data records"""
    __tablename__ = "clinical_data_records"

    clinical_data_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        comment="Unique clinical data identifier"
    )
    session_id = Column(
        String(255),
        nullable=False,
        index=True,
        comment="Session identifier"
    )
    transcript_id = Column(
        UUID(as_uuid=True),
        ForeignKey("transcripts.transcript_id"),
        nullable=False,
        index=True,
        comment="Associated transcript ID"
    )
    extracted_data = Column(
        JSONB,
        nullable=False,
        comment="Extracted clinical data (encrypted)"
    )
    validated_data = Column(
        JSONB,
        nullable=True,
        comment="Validated assessment data (encrypted)"
    )
    validation_status = Column(
        JSONB,
        nullable=False,
        comment="Validation status metadata"
    )
    validated_by = Column(
        String(255),
        nullable=True,
        index=True,
        comment="Validator identifier"
    )
    validated_at = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Validation timestamp"
    )
    submission_id = Column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
        comment="Associated submission ID"
    )
    status = Column(
        Enum(ClinicalDataStatus, name="clinical_data_status_enum"),
        nullable=False,
        default=ClinicalDataStatus.DRAFT,
        comment="Record status"
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
    transcript = relationship("Transcript", backref="clinical_data_records")

    def __repr__(self):
        return f"<ClinicalDataRecord(clinical_data_id={self.clinical_data_id}, session_id={self.session_id})>"
