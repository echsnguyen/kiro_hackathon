"""Pydantic schemas for clinical data extraction"""

from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class SourceSegment(BaseModel):
    """Schema for source segment reference"""
    segment_id: str = Field(..., description="Segment identifier")
    text: str = Field(..., description="Segment text")
    start_time: float = Field(..., ge=0, description="Start time in seconds")
    end_time: float = Field(..., ge=0, description="End time in seconds")
    speaker: str = Field(..., description="Speaker identifier")


class FieldExtraction(BaseModel):
    """Schema for extracted field with metadata"""
    value: str = Field(..., description="Extracted value")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score")
    source_segments: List[SourceSegment] = Field(
        default_factory=list, description="Source transcript segments"
    )
    flagged_for_review: bool = Field(
        False, description="Whether field is flagged for review"
    )


class Demographics(BaseModel):
    """Schema for demographics data"""
    name: Optional[FieldExtraction] = Field(None, description="Client name")
    age: Optional[FieldExtraction] = Field(None, description="Client age")
    living_arrangements: Optional[FieldExtraction] = Field(
        None, description="Living arrangements"
    )


class ClinicalHistory(BaseModel):
    """Schema for clinical history data"""
    current_medications: List[FieldExtraction] = Field(
        default_factory=list, description="Current medications"
    )
    past_surgeries: List[FieldExtraction] = Field(
        default_factory=list, description="Past surgeries"
    )
    chronic_conditions: List[FieldExtraction] = Field(
        default_factory=list, description="Chronic conditions"
    )


class FunctionalStatus(BaseModel):
    """Schema for functional status data"""
    mobility: Optional[FieldExtraction] = Field(None, description="Mobility status")
    falls_history: Optional[FieldExtraction] = Field(None, description="Falls history")
    adls: List[FieldExtraction] = Field(
        default_factory=list, description="Activities of Daily Living"
    )


class GoalsAspirations(BaseModel):
    """Schema for goals and aspirations data"""
    goals: List[FieldExtraction] = Field(
        default_factory=list, description="Client goals and aspirations"
    )


class RiskAssessment(BaseModel):
    """Schema for risk assessment data"""
    cognitive_state: Optional[FieldExtraction] = Field(
        None, description="Cognitive state assessment"
    )
    skin_integrity: Optional[FieldExtraction] = Field(
        None, description="Skin integrity assessment"
    )
    nutritional_risks: Optional[FieldExtraction] = Field(
        None, description="Nutritional risk assessment"
    )


class ExtractionMetadata(BaseModel):
    """Schema for extraction metadata"""
    model_version: str = Field(..., description="LLM model version")
    extraction_time: datetime = Field(..., description="Extraction timestamp")
    overall_confidence: float = Field(
        ..., ge=0, le=1, description="Overall confidence score"
    )
    flagged_field_count: int = Field(
        ..., ge=0, description="Number of flagged fields"
    )


class ExtractedClinicalData(BaseModel):
    """Schema for extracted clinical data"""
    session_id: str = Field(..., description="Session identifier")
    demographics: Demographics = Field(..., description="Demographics data")
    clinical_history: ClinicalHistory = Field(..., description="Clinical history data")
    functional_status: FunctionalStatus = Field(..., description="Functional status data")
    goals_aspirations: GoalsAspirations = Field(
        ..., description="Goals and aspirations data"
    )
    risk_assessment: RiskAssessment = Field(..., description="Risk assessment data")
    extraction_metadata: ExtractionMetadata = Field(..., description="Extraction metadata")


class ClinicalDataRecordBase(BaseModel):
    """Base clinical data record schema"""
    session_id: str = Field(..., description="Session identifier")
    transcript_id: str = Field(..., description="Associated transcript ID")


class ClinicalDataRecordCreate(ClinicalDataRecordBase):
    """Schema for creating a clinical data record"""
    extracted_data: ExtractedClinicalData = Field(..., description="Extracted data")


class ValidationStatus(BaseModel):
    """Schema for validation status"""
    total_fields: int = Field(..., ge=0, description="Total number of fields")
    validated_fields: int = Field(..., ge=0, description="Number of validated fields")
    flagged_fields: int = Field(..., ge=0, description="Number of flagged fields")
    ready_for_submission: bool = Field(..., description="Whether ready for submission")


class ClinicalDataRecordResponse(ClinicalDataRecordBase):
    """Schema for clinical data record response"""
    clinical_data_id: str = Field(..., description="Unique clinical data identifier")
    extracted_data: ExtractedClinicalData = Field(..., description="Extracted data")
    validated_data: Optional[dict] = Field(None, description="Validated data")
    validation_status: ValidationStatus = Field(..., description="Validation status")
    validated_by: Optional[str] = Field(None, description="Validator identifier")
    validated_at: Optional[datetime] = Field(None, description="Validation timestamp")
    submission_id: Optional[str] = Field(None, description="Submission identifier")
    status: Literal["draft", "validated", "submitted"] = Field(
        ..., description="Record status"
    )
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Record update timestamp")

    model_config = {"from_attributes": True}


class FieldExtractionRequest(BaseModel):
    """Schema for field re-extraction request"""
    field_name: str = Field(..., description="Field name to re-extract")


class ValidationResult(BaseModel):
    """Schema for extraction validation result"""
    is_valid: bool = Field(..., description="Whether extraction is valid")
    errors: List[str] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
