# Requirements Document

## Introduction

The AI Allied Health Assessment Automator is an integrated clinical documentation tool that transforms audio recordings of client consultations into structured, validated assessment data. The system captures consultation audio, transcribes it with medical vocabulary support, extracts clinical entities using LLM technology, and presents the data for clinician review before integration with the provider portal. This automation reduces manual data entry burden while maintaining clinical accuracy and compliance with health data privacy regulations.

## Glossary

- **System**: The AI Allied Health Assessment Automator
- **Clinician**: Healthcare provider conducting the assessment (employee)
- **Client**: Person receiving allied health services
- **Carer**: Family member or support person accompanying the Client
- **Assessment_Form**: Initial Assessment Form within the provider portal
- **Portal**: Existing provider portal system with database
- **Transcript**: Text output from Speech-to-Text processing
- **Draft_Mode**: Review state where auto-populated data awaits clinician validation
- **Diarization**: Process of distinguishing between different speakers in audio
- **PII**: Personally Identifiable Information
- **PHI**: Personal Health Information
- **STT**: Speech-to-Text engine
- **WER**: Word Error Rate (accuracy metric for transcription)
- **ADL**: Activities of Daily Living
- **APP**: Australian Privacy Principles
- **HIPAA**: Health Insurance Portability and Accountability Act

## Requirements

### Requirement 1: Audio Capture

**User Story:** As a clinician, I want to securely record client consultations via mobile or tablet, so that I can capture the full conversation for automated processing.

#### Acceptance Criteria

1. WHEN a clinician initiates recording, THE System SHALL capture audio in a format suitable for medical transcription
2. WHEN recording is active, THE System SHALL provide visual feedback indicating recording status
3. WHEN recording is complete, THE System SHALL encrypt the audio file using AES-256 encryption at rest
4. WHEN audio capture fails, THE System SHALL notify the clinician and preserve any partial recording
5. THE System SHALL support audio recording on mobile, tablet, laptop, and desktop computer interfaces

### Requirement 2: Consent Management

**User Story:** As a clinician, I want to obtain and record client consent before recording, so that I comply with privacy regulations and ethical standards.

#### Acceptance Criteria

1. WHEN a clinician starts a new consultation session, THE System SHALL present a consent interface before enabling recording
2. THE System SHALL support both digital signature and verbal consent with timestamp
3. WHEN consent is provided, THE System SHALL store the consent record with timestamp and method
4. IF consent is not obtained, THEN THE System SHALL prevent audio recording
5. WHEN consent records are stored, THE System SHALL encrypt them using AES-256 encryption

### Requirement 3: Speech-to-Text Transcription

**User Story:** As a clinician, I want high-accuracy transcription of consultation audio including medical terminology, so that the extracted data reflects what was actually discussed.

#### Acceptance Criteria

1. WHEN audio is submitted for transcription, THE System SHALL process it using a medical-vocabulary-aware STT engine
2. THE System SHALL achieve transcription accuracy suitable for elderly voices and clinical terminology
3. WHEN transcription is complete, THE System SHALL deliver results within 30 seconds for typical consultation length
4. WHERE streaming transcription is supported, THE System SHALL provide real-time transcript updates
5. WHEN recording is active, THE System SHALL display a live view of the Transcript as it is being generated
6. WHEN transcription is complete, THE System SHALL save the Transcript for future reference
7. WHEN transcription fails, THE System SHALL notify the clinician and preserve the original audio for retry

### Requirement 4: Speaker Diarization

**User Story:** As a clinician, I want the system to distinguish between my voice, the client's voice, and any carer's voice, so that I can understand who said what during the consultation.

#### Acceptance Criteria

1. WHEN audio contains multiple speakers, THE System SHALL identify and label distinct speakers
2. THE System SHALL distinguish between Clinician, Client, and Carer voices
3. WHEN diarization is complete, THE System SHALL annotate the Transcript with speaker labels
4. WHEN speaker identification is uncertain, THE System SHALL mark ambiguous segments for clinician review
5. THE System SHALL maintain speaker consistency throughout the entire Transcript

### Requirement 5: Clinical Data Extraction

**User Story:** As a clinician, I want the system to automatically extract structured clinical information from the transcript, so that I don't have to manually type assessment data.

#### Acceptance Criteria

1. WHEN a Transcript is available, THE System SHALL extract demographics including name, age, and living arrangements
2. WHEN a Transcript is available, THE System SHALL extract clinical history including current medications, past surgeries, and chronic conditions
3. WHEN a Transcript is available, THE System SHALL extract functional status including mobility, falls history, and ADLs
4. WHEN a Transcript is available, THE System SHALL extract client goals and aspirations
5. WHEN a Transcript is available, THE System SHALL extract risk assessment data including cognitive state, skin integrity, and nutritional risks
6. THE System SHALL output extracted data in JSON format matching Assessment_Form field structure
7. WHEN extraction confidence is low for any field, THE System SHALL flag that field for clinician attention

### Requirement 6: Review Interface

**User Story:** As a clinician, I want to review auto-populated assessment data alongside the source transcript, so that I can verify accuracy before submission.

#### Acceptance Criteria

1. WHEN extraction is complete, THE System SHALL present a side-by-side interface showing Transcript and auto-populated Assessment_Form fields
2. WHEN a clinician clicks on any form field, THE System SHALL highlight the source text in the Transcript that generated that field value
3. THE System SHALL display all auto-populated data in Draft_Mode requiring explicit clinician validation
4. WHEN a clinician edits a form field, THE System SHALL preserve the edit and mark the field as manually validated
5. THE System SHALL allow clinicians to highlight Transcript segments and manually assign them to form fields
6. WHEN all required fields are validated, THE System SHALL enable the submit action

### Requirement 7: Data Security and Encryption

**User Story:** As a system administrator, I want all health data encrypted in transit and at rest, so that we comply with APP and HIPAA requirements.

#### Acceptance Criteria

1. THE System SHALL encrypt all audio files using AES-256 encryption at rest
2. THE System SHALL encrypt all transcript data using AES-256 encryption at rest
3. THE System SHALL encrypt all extracted clinical data using AES-256 encryption at rest
4. THE System SHALL use TLS 1.2 or higher for all data transmission
5. WHEN data is transmitted to the Portal, THE System SHALL use encrypted connections
6. THE System SHALL encrypt consent records using AES-256 encryption at rest

### Requirement 8: PII Redaction

**User Story:** As a privacy officer, I want highly sensitive information automatically redacted from stored data, so that we minimize privacy risk.

#### Acceptance Criteria

1. WHERE PII redaction is enabled, THE System SHALL identify highly sensitive information in transcripts
2. WHERE PII redaction is enabled, THE System SHALL redact identified sensitive information before storage
3. WHEN PII is redacted, THE System SHALL maintain sufficient context for clinical utility
4. THE System SHALL allow clinicians to review and override redaction decisions
5. WHEN redaction occurs, THE System SHALL log the redaction event for audit purposes

### Requirement 9: Zero Data Retention Policy

**User Story:** As a privacy officer, I want assurance that no consultation data is used for model training, so that we maintain client confidentiality.

#### Acceptance Criteria

1. THE System SHALL operate using private instances of STT and LLM services
2. THE System SHALL configure all AI services with zero data retention policies
3. THE System SHALL not transmit any consultation data to services that perform model training
4. WHEN AI services are configured, THE System SHALL verify and document their data retention policies
5. THE System SHALL maintain audit logs confirming no data was retained by external services

### Requirement 10: Portal Integration

**User Story:** As a clinician, I want to submit validated assessment data directly to the provider portal with one click, so that I can complete documentation efficiently.

#### Acceptance Criteria

1. WHEN a clinician approves validated data, THE System SHALL format the data as a JSON payload matching Portal API specifications
2. WHEN submission is initiated, THE System SHALL transmit data to the Portal via RESTful API
3. WHEN Portal integration succeeds, THE System SHALL confirm successful submission to the clinician
4. IF Portal integration fails, THEN THE System SHALL preserve the validated data and allow retry
5. WHEN data is transmitted to the Portal, THE System SHALL use TLS 1.2 or higher encryption
6. THE System SHALL log all submission attempts with timestamps and status for audit purposes

### Requirement 11: Human-in-the-Loop Safety

**User Story:** As a clinical director, I want to ensure AI never auto-submits assessment data without clinician review, so that we maintain clinical accountability.

#### Acceptance Criteria

1. THE System SHALL never automatically submit data to the Portal without explicit clinician approval
2. THE System SHALL present all auto-populated data in Draft_Mode by default
3. WHEN data is in Draft_Mode, THE System SHALL disable automatic submission
4. THE System SHALL require explicit clinician action to transition from Draft_Mode to submission
5. WHEN submission is attempted without validation, THE System SHALL prevent submission and prompt for review

### Requirement 12: Error Handling and Recovery

**User Story:** As a clinician, I want the system to handle failures gracefully and preserve my work, so that I don't lose consultation data due to technical issues.

#### Acceptance Criteria

1. WHEN any processing step fails, THE System SHALL preserve all data from previous successful steps
2. WHEN transcription fails, THE System SHALL retain the original audio and allow manual retry
3. WHEN extraction fails, THE System SHALL retain the Transcript and allow manual data entry
4. WHEN Portal submission fails, THE System SHALL retain validated data and provide retry options
5. THE System SHALL provide clear error messages indicating what failed and what actions are available
6. WHEN network connectivity is lost, THE System SHALL queue data for submission when connectivity is restored

### Requirement 13: Performance and Latency

**User Story:** As a clinician, I want fast processing of consultation recordings, so that I can complete documentation during or immediately after the consultation.

#### Acceptance Criteria

1. WHEN audio is submitted for transcription, THE System SHALL complete processing within 30 seconds for typical consultation length
2. WHEN transcription is complete, THE System SHALL begin extraction immediately without manual intervention
3. WHEN extraction is complete, THE System SHALL display the review interface within 5 seconds
4. THE System SHALL provide progress indicators during all processing steps
5. WHERE streaming transcription is available, THE System SHALL display transcript updates in real-time

### Requirement 14: Audit Logging

**User Story:** As a compliance officer, I want comprehensive audit logs of all system actions, so that we can demonstrate regulatory compliance and investigate issues.

#### Acceptance Criteria

1. WHEN consent is obtained, THE System SHALL log the consent event with timestamp, method, and user
2. WHEN audio is recorded, THE System SHALL log the recording event with timestamp, duration, and user
3. WHEN transcription occurs, THE System SHALL log the transcription event with timestamp and processing time
4. WHEN data is extracted, THE System SHALL log the extraction event with timestamp and confidence scores
5. WHEN data is edited, THE System SHALL log the edit event with timestamp, field, and user
6. WHEN data is submitted to Portal, THE System SHALL log the submission event with timestamp, status, and user
7. THE System SHALL encrypt all audit logs using AES-256 encryption at rest
8. THE System SHALL retain audit logs according to regulatory requirements

### Requirement 15: Manual Override and Snippet Assignment

**User Story:** As a clinician, I want to manually assign transcript segments to form fields when AI misses nuances, so that I can ensure accurate documentation.

#### Acceptance Criteria

1. WHEN a clinician highlights text in the Transcript, THE System SHALL enable manual field assignment
2. WHEN a clinician assigns a transcript segment to a field, THE System SHALL populate that field with the selected text
3. WHEN a field has both AI-extracted and manually-assigned content, THE System SHALL prioritize the manual assignment
4. THE System SHALL allow clinicians to assign multiple transcript segments to a single field
5. WHEN manual assignment occurs, THE System SHALL mark the field as manually validated
6. THE System SHALL preserve the link between form fields and their source transcript segments for audit purposes
