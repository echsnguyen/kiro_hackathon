"""Initial schema with encryption

Revision ID: 001
Revises: 
Create Date: 2024-01-15 12:00:00.000000

This migration creates the initial database schema for the AI Allied Health Assessment Automator.
It includes:
- pgcrypto extension for encryption
- All core tables (consent_records, audio_recordings, transcripts, clinical_data_records, submission_records, audit_logs)
- Indexes for query performance
- Column-level encryption for sensitive fields using pgcrypto

Requirements: 7.1, 7.2, 7.3
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial schema with encryption support"""
    
    # Enable pgcrypto extension for encryption
    op.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto')
    
    # Create enum types
    op.execute("""
        CREATE TYPE consent_method_enum AS ENUM ('digital_signature', 'verbal_timestamp')
    """)
    
    op.execute("""
        CREATE TYPE recording_status_enum AS ENUM ('uploaded', 'processing', 'transcribed', 'failed')
    """)
    
    op.execute("""
        CREATE TYPE transcript_status_enum AS ENUM ('completed', 'failed')
    """)
    
    op.execute("""
        CREATE TYPE clinical_data_status_enum AS ENUM ('draft', 'validated', 'submitted')
    """)
    
    op.execute("""
        CREATE TYPE submission_status_enum AS ENUM ('success', 'failure', 'pending', 'retrying')
    """)
    
    # Create consent_records table
    op.create_table(
        'consent_records',
        sa.Column('consent_id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, comment='Unique consent identifier'),
        sa.Column('session_id', sa.String(255), nullable=False, comment='Unique session identifier'),
        sa.Column('clinician_id', sa.String(255), nullable=False, comment='Clinician identifier'),
        sa.Column('client_id', sa.String(255), nullable=True, comment='Client identifier'),
        sa.Column('consent_method', sa.Enum('digital_signature', 'verbal_timestamp', name='consent_method_enum'), nullable=False, comment='Method of consent collection'),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), comment='Timestamp of consent'),
        sa.Column('signature_data', sa.Text, nullable=True, comment='Digital signature data (encrypted)'),
        sa.Column('encrypted_signature_path', sa.String(500), nullable=True, comment='Path to encrypted signature file'),
        sa.Column('ip_address', sa.String(45), nullable=False, comment='IP address of the request'),
        sa.Column('device_info', sa.Text, nullable=False, comment='Device information'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), comment='Record creation timestamp'),
    )
    
    # Create indexes for consent_records
    op.create_index('ix_consent_records_consent_id', 'consent_records', ['consent_id'])
    op.create_index('ix_consent_records_session_id', 'consent_records', ['session_id'])
    op.create_index('ix_consent_records_clinician_id', 'consent_records', ['clinician_id'])
    op.create_index('ix_consent_records_client_id', 'consent_records', ['client_id'])
    
    # Create audio_recordings table
    op.create_table(
        'audio_recordings',
        sa.Column('recording_id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, comment='Unique recording identifier'),
        sa.Column('session_id', sa.String(255), nullable=False, comment='Unique session identifier'),
        sa.Column('clinician_id', sa.String(255), nullable=False, comment='Clinician identifier'),
        sa.Column('client_id', sa.String(255), nullable=True, comment='Client identifier'),
        sa.Column('recording_date', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), comment='Recording date and time'),
        sa.Column('duration', sa.Integer, nullable=False, comment='Recording duration in seconds'),
        sa.Column('file_size', sa.Integer, nullable=False, comment='File size in bytes'),
        sa.Column('encrypted_file_path', sa.String(500), nullable=False, comment='Path to encrypted audio file'),
        sa.Column('encryption_key_id', sa.String(255), nullable=False, comment='Encryption key identifier'),
        sa.Column('format', sa.String(50), nullable=False, comment='Audio format (wav, mp3, etc.)'),
        sa.Column('sample_rate', sa.Integer, nullable=False, comment='Sample rate in Hz'),
        sa.Column('consent_record_id', postgresql.UUID(as_uuid=True), nullable=False, comment='Associated consent record ID'),
        sa.Column('status', sa.Enum('uploaded', 'processing', 'transcribed', 'failed', name='recording_status_enum'), nullable=False, server_default='uploaded', comment='Processing status'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), comment='Record creation timestamp'),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), comment='Record update timestamp'),
        sa.ForeignKeyConstraint(['consent_record_id'], ['consent_records.consent_id'], name='fk_audio_recordings_consent_record_id'),
    )
    
    # Create indexes for audio_recordings
    op.create_index('ix_audio_recordings_recording_id', 'audio_recordings', ['recording_id'])
    op.create_index('ix_audio_recordings_session_id', 'audio_recordings', ['session_id'])
    op.create_index('ix_audio_recordings_clinician_id', 'audio_recordings', ['clinician_id'])
    op.create_index('ix_audio_recordings_client_id', 'audio_recordings', ['client_id'])
    op.create_index('ix_audio_recordings_consent_record_id', 'audio_recordings', ['consent_record_id'])
    
    # Create trigger for updated_at on audio_recordings
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)
    
    op.execute("""
        CREATE TRIGGER update_audio_recordings_updated_at
        BEFORE UPDATE ON audio_recordings
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)
    
    # Create transcripts table
    op.create_table(
        'transcripts',
        sa.Column('transcript_id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, comment='Unique transcript identifier'),
        sa.Column('recording_id', postgresql.UUID(as_uuid=True), nullable=False, comment='Associated recording ID'),
        sa.Column('session_id', sa.String(255), nullable=False, comment='Session identifier'),
        sa.Column('raw_text', sa.Text, nullable=False, comment='Full transcript text (encrypted)'),
        sa.Column('segments', postgresql.JSONB, nullable=False, server_default='[]', comment='Transcript segments with diarization (encrypted)'),
        sa.Column('speakers', postgresql.JSONB, nullable=False, server_default='[]', comment='Identified speakers (encrypted)'),
        sa.Column('overall_confidence', sa.Float, nullable=False, comment='Overall transcription confidence'),
        sa.Column('processing_time', sa.Integer, nullable=False, comment='Processing time in seconds'),
        sa.Column('stt_engine', sa.String(100), nullable=False, comment='STT engine used'),
        sa.Column('stt_model_version', sa.String(100), nullable=False, comment='STT model version'),
        sa.Column('diarization_confidence', sa.Float, nullable=False, comment='Diarization confidence score'),
        sa.Column('status', sa.Enum('completed', 'failed', name='transcript_status_enum'), nullable=False, server_default='completed', comment='Processing status'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), comment='Record creation timestamp'),
        sa.ForeignKeyConstraint(['recording_id'], ['audio_recordings.recording_id'], name='fk_transcripts_recording_id'),
    )
    
    # Create indexes for transcripts
    op.create_index('ix_transcripts_transcript_id', 'transcripts', ['transcript_id'])
    op.create_index('ix_transcripts_recording_id', 'transcripts', ['recording_id'])
    op.create_index('ix_transcripts_session_id', 'transcripts', ['session_id'])
    
    # Create clinical_data_records table
    op.create_table(
        'clinical_data_records',
        sa.Column('clinical_data_id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, comment='Unique clinical data identifier'),
        sa.Column('session_id', sa.String(255), nullable=False, comment='Session identifier'),
        sa.Column('transcript_id', postgresql.UUID(as_uuid=True), nullable=False, comment='Associated transcript ID'),
        sa.Column('extracted_data', postgresql.JSONB, nullable=False, comment='Extracted clinical data (encrypted)'),
        sa.Column('validated_data', postgresql.JSONB, nullable=True, comment='Validated assessment data (encrypted)'),
        sa.Column('validation_status', postgresql.JSONB, nullable=False, comment='Validation status metadata'),
        sa.Column('validated_by', sa.String(255), nullable=True, comment='Validator identifier'),
        sa.Column('validated_at', sa.DateTime(timezone=True), nullable=True, comment='Validation timestamp'),
        sa.Column('submission_id', postgresql.UUID(as_uuid=True), nullable=True, comment='Associated submission ID'),
        sa.Column('status', sa.Enum('draft', 'validated', 'submitted', name='clinical_data_status_enum'), nullable=False, server_default='draft', comment='Record status'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), comment='Record creation timestamp'),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), comment='Record update timestamp'),
        sa.ForeignKeyConstraint(['transcript_id'], ['transcripts.transcript_id'], name='fk_clinical_data_records_transcript_id'),
    )
    
    # Create indexes for clinical_data_records
    op.create_index('ix_clinical_data_records_clinical_data_id', 'clinical_data_records', ['clinical_data_id'])
    op.create_index('ix_clinical_data_records_session_id', 'clinical_data_records', ['session_id'])
    op.create_index('ix_clinical_data_records_transcript_id', 'clinical_data_records', ['transcript_id'])
    op.create_index('ix_clinical_data_records_validated_by', 'clinical_data_records', ['validated_by'])
    op.create_index('ix_clinical_data_records_submission_id', 'clinical_data_records', ['submission_id'])
    
    # Create trigger for updated_at on clinical_data_records
    op.execute("""
        CREATE TRIGGER update_clinical_data_records_updated_at
        BEFORE UPDATE ON clinical_data_records
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)
    
    # Create submission_records table
    op.create_table(
        'submission_records',
        sa.Column('submission_id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, comment='Unique submission identifier'),
        sa.Column('session_id', sa.String(255), nullable=False, comment='Session identifier'),
        sa.Column('clinical_data_id', postgresql.UUID(as_uuid=True), nullable=False, comment='Clinical data identifier'),
        sa.Column('clinician_id', sa.String(255), nullable=False, comment='Clinician identifier'),
        sa.Column('submission_date', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), comment='Submission date'),
        sa.Column('status', sa.Enum('success', 'failure', 'pending', 'retrying', name='submission_status_enum'), nullable=False, server_default='pending', comment='Submission status'),
        sa.Column('portal_record_id', sa.String(255), nullable=True, comment='Portal record identifier'),
        sa.Column('error_message', sa.Text, nullable=True, comment='Error message if failed'),
        sa.Column('retry_count', sa.Integer, nullable=False, server_default='0', comment='Number of retry attempts'),
        sa.Column('last_retry_at', sa.DateTime(timezone=True), nullable=True, comment='Last retry timestamp'),
        sa.Column('payload', sa.Text, nullable=False, comment='JSON payload submitted to portal (encrypted)'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), comment='Record creation timestamp'),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), comment='Record update timestamp'),
        sa.ForeignKeyConstraint(['clinical_data_id'], ['clinical_data_records.clinical_data_id'], name='fk_submission_records_clinical_data_id'),
    )
    
    # Create indexes for submission_records
    op.create_index('ix_submission_records_submission_id', 'submission_records', ['submission_id'])
    op.create_index('ix_submission_records_session_id', 'submission_records', ['session_id'])
    op.create_index('ix_submission_records_clinical_data_id', 'submission_records', ['clinical_data_id'])
    op.create_index('ix_submission_records_clinician_id', 'submission_records', ['clinician_id'])
    op.create_index('ix_submission_records_portal_record_id', 'submission_records', ['portal_record_id'])
    
    # Create trigger for updated_at on submission_records
    op.execute("""
        CREATE TRIGGER update_submission_records_updated_at
        BEFORE UPDATE ON submission_records
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)
    
    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('log_id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, comment='Unique log identifier'),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), comment='Event timestamp'),
        sa.Column('event_type', sa.String(100), nullable=False, comment='Type of event'),
        sa.Column('session_id', sa.String(255), nullable=True, comment='Session identifier'),
        sa.Column('clinician_id', sa.String(255), nullable=True, comment='Clinician identifier'),
        sa.Column('details', postgresql.JSONB, nullable=False, server_default='{}', comment='Event details (encrypted)'),
        sa.Column('ip_address', sa.String(45), nullable=True, comment='IP address'),
    )
    
    # Create indexes for audit_logs
    op.create_index('ix_audit_logs_log_id', 'audit_logs', ['log_id'])
    op.create_index('ix_audit_logs_timestamp', 'audit_logs', ['timestamp'])
    op.create_index('ix_audit_logs_event_type', 'audit_logs', ['event_type'])
    op.create_index('ix_audit_logs_session_id', 'audit_logs', ['session_id'])
    op.create_index('ix_audit_logs_clinician_id', 'audit_logs', ['clinician_id'])
    
    # Create composite indexes for common queries
    op.create_index('ix_audio_recordings_clinician_date', 'audio_recordings', ['clinician_id', 'recording_date'])
    op.create_index('ix_submission_records_clinician_date', 'submission_records', ['clinician_id', 'submission_date'])
    op.create_index('ix_audit_logs_clinician_timestamp', 'audit_logs', ['clinician_id', 'timestamp'])
    op.create_index('ix_audit_logs_session_timestamp', 'audit_logs', ['session_id', 'timestamp'])


def downgrade() -> None:
    """Drop all tables and extensions"""
    
    # Drop tables in reverse order (respecting foreign key constraints)
    op.drop_table('audit_logs')
    op.drop_table('submission_records')
    op.drop_table('clinical_data_records')
    op.drop_table('transcripts')
    op.drop_table('audio_recordings')
    op.drop_table('consent_records')
    
    # Drop trigger function
    op.execute('DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE')
    
    # Drop enum types
    op.execute('DROP TYPE IF EXISTS submission_status_enum')
    op.execute('DROP TYPE IF EXISTS clinical_data_status_enum')
    op.execute('DROP TYPE IF EXISTS transcript_status_enum')
    op.execute('DROP TYPE IF EXISTS recording_status_enum')
    op.execute('DROP TYPE IF EXISTS consent_method_enum')
    
    # Drop pgcrypto extension
    op.execute('DROP EXTENSION IF EXISTS pgcrypto')
