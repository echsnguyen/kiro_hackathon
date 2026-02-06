"""SQLAlchemy ORM models for consent management"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.database import Base


class ConsentMethod(str, enum.Enum):
    """Enum for consent methods"""
    DIGITAL_SIGNATURE = "digital_signature"
    VERBAL_TIMESTAMP = "verbal_timestamp"


class ConsentRecord(Base):
    """ORM model for consent records"""
    __tablename__ = "consent_records"

    consent_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        comment="Unique consent identifier"
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
    consent_method = Column(
        Enum(ConsentMethod, name="consent_method_enum"),
        nullable=False,
        comment="Method of consent collection"
    )
    timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        comment="Timestamp of consent"
    )
    signature_data = Column(
        Text,
        nullable=True,
        comment="Digital signature data (encrypted)"
    )
    encrypted_signature_path = Column(
        String(500),
        nullable=True,
        comment="Path to encrypted signature file"
    )
    ip_address = Column(
        String(45),
        nullable=False,
        comment="IP address of the request"
    )
    device_info = Column(
        Text,
        nullable=False,
        comment="Device information"
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        comment="Record creation timestamp"
    )

    def __repr__(self):
        return f"<ConsentRecord(consent_id={self.consent_id}, session_id={self.session_id})>"
