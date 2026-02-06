"""Pydantic schemas for portal submission"""

from datetime import datetime
from typing import Any, Dict, Literal, Optional
from pydantic import BaseModel, Field


class SubmissionMetadata(BaseModel):
    """Schema for submission metadata"""
    source_system: str = Field(..., description="Source system identifier")
    source_version: str = Field(..., description="Source system version")
    submission_method: Literal["automated"] = Field(
        "automated", description="Submission method"
    )
    validated_by: str = Field(..., description="Validator identifier")
    validation_timestamp: datetime = Field(..., description="Validation timestamp")


class AssessmentFormData(BaseModel):
    """Schema for assessment form data"""
    demographics: Dict[str, Any] = Field(..., description="Demographics data")
    clinical_history: Dict[str, Any] = Field(..., description="Clinical history data")
    functional_status: Dict[str, Any] = Field(..., description="Functional status data")
    goals_aspirations: Dict[str, Any] = Field(..., description="Goals and aspirations data")
    risk_assessment: Dict[str, Any] = Field(..., description="Risk assessment data")


class ValidatedAssessmentData(BaseModel):
    """Schema for validated assessment data"""
    session_id: str = Field(..., description="Session identifier")
    clinician_id: str = Field(..., description="Clinician identifier")
    client_id: str = Field(..., description="Client identifier")
    assessment_date: datetime = Field(..., description="Assessment date")
    form_data: AssessmentFormData = Field(..., description="Form data")
    metadata: SubmissionMetadata = Field(..., description="Submission metadata")


class SubmissionResult(BaseModel):
    """Schema for submission result"""
    submission_id: str = Field(..., description="Unique submission identifier")
    status: Literal["success", "failure", "pending"] = Field(..., description="Submission status")
    portal_record_id: Optional[str] = Field(None, description="Portal record identifier")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    timestamp: datetime = Field(..., description="Submission timestamp")


class SubmissionStatus(BaseModel):
    """Schema for submission status query"""
    submission_id: str = Field(..., description="Submission identifier")
    status: Literal["success", "failure", "pending", "retrying"] = Field(
        ..., description="Current status"
    )
    retry_count: int = Field(..., ge=0, description="Number of retry attempts")
    last_retry_at: Optional[datetime] = Field(None, description="Last retry timestamp")
    error_message: Optional[str] = Field(None, description="Error message if failed")


class SubmissionRecordBase(BaseModel):
    """Base submission record schema"""
    session_id: str = Field(..., description="Session identifier")
    clinical_data_id: str = Field(..., description="Clinical data identifier")
    clinician_id: str = Field(..., description="Clinician identifier")


class SubmissionRecordCreate(SubmissionRecordBase):
    """Schema for creating a submission record"""
    payload: str = Field(..., description="JSON payload submitted to portal")


class SubmissionRecordResponse(SubmissionRecordBase):
    """Schema for submission record response"""
    submission_id: str = Field(..., description="Unique submission identifier")
    submission_date: datetime = Field(..., description="Submission date")
    status: Literal["success", "failure", "pending", "retrying"] = Field(
        ..., description="Submission status"
    )
    portal_record_id: Optional[str] = Field(None, description="Portal record identifier")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    retry_count: int = Field(..., ge=0, description="Number of retry attempts")
    last_retry_at: Optional[datetime] = Field(None, description="Last retry timestamp")
    payload: str = Field(..., description="JSON payload")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Record update timestamp")

    model_config = {"from_attributes": True}
