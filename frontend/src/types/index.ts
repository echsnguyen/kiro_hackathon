// Core types for ECH Scribe

export type InputMethod = 'live-recording' | 'audio-upload' | 'transcript-upload';

export type WorkflowStep = 'input-choice' | 'consent' | 'record' | 'transcribe' | 'extract' | 'review' | 'submit';

export interface ConsentRecord {
  sessionId: string;
  consentMethod: 'digital_signature' | 'verbal_timestamp';
  timestamp: Date;
  clinicianId: string;
  clientId?: string;
  signatureData?: string;
}

export interface TranscriptSegment {
  id: number;
  speaker: 'clinician' | 'client' | 'carer';
  text: string;
  startTime: number;
  endTime: number;
  linkedFields: string[];
}

export interface FormField {
  id: string;
  label: string;
  value: string;
  confidence: number;
  flagged: boolean;
  category: string;
}

export interface ValidationStatus {
  totalFields: number;
  validatedFields: number;
  flaggedFields: number;
  readyForSubmission: boolean;
}

export interface WorkflowConfiguration {
  method: InputMethod;
  requiresConsent: boolean;
  requiresTranscription: boolean;
  steps: {
    id: WorkflowStep;
    title: string;
    visible: boolean;
    completed: boolean;
  }[];
}
