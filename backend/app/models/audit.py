"""SQLAlchemy ORM models for audit logging"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.database import Base


class AuditLog(Base):
    """ORM model for audit logs"""
    __tablename__ = "audit_logs"

    log_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        comment="Unique log identifier"
    )
    timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        index=True,
        comment="Event timestamp"
    )
    event_type = Column(
        String(100),
        nullable=False,
        index=True,
        comment="Type of event"
    )
    session_id = Column(
        String(255),
        nullable=True,
        index=True,
        comment="Session identifier"
    )
    clinician_id = Column(
        String(255),
        nullable=True,
        index=True,
        comment="Clinician identifier"
    )
    details = Column(
        JSONB,
        nullable=False,
        default=dict,
        comment="Event details (encrypted)"
    )
    ip_address = Column(
        String(45),
        nullable=True,
        comment="IP address"
    )

    def __repr__(self):
        return f"<AuditLog(log_id={self.log_id}, event_type={self.event_type})>"
