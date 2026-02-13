import { useState } from 'react';
import InputMethodSelector from './components/InputMethodSelector';
import { InputMethod, WorkflowStep } from './types';
import './App.css';

function App() {
  const [currentStep, setCurrentStep] = useState<WorkflowStep>('input-choice');
  const [selectedMethod, setSelectedMethod] = useState<InputMethod | null>(null);
  const [completedSteps, setCompletedSteps] = useState<Set<WorkflowStep>>(new Set());

  const workflowSteps: { id: WorkflowStep; title: string; number: number }[] = [
    { id: 'input-choice', title: 'Input Method', number: 1 },
    { id: 'consent', title: 'Consent', number: 2 },
    { id: 'record', title: 'Record/Upload', number: 3 },
    { id: 'transcribe', title: 'Transcribe', number: 4 },
    { id: 'extract', title: 'Extract', number: 5 },
    { id: 'review', title: 'Review', number: 6 },
    { id: 'submit', title: 'Submit', number: 7 },
  ];

  const isStepVisible = (stepId: WorkflowStep): boolean => {
    if (!selectedMethod) return true;
    
    if (stepId === 'consent') {
      return selectedMethod === 'live-recording';
    }
    if (stepId === 'transcribe') {
      return selectedMethod !== 'transcript-upload';
    }
    return true;
  };

  const handleMethodSelect = (method: InputMethod) => {
    setSelectedMethod(method);
    setCompletedSteps(new Set(['input-choice']));
    
    if (method === 'live-recording') {
      setCurrentStep('consent');
    } else {
      setCurrentStep('record');
    }
  };

  const handleStepClick = (stepId: WorkflowStep) => {
    if (isStepVisible(stepId)) {
      setCurrentStep(stepId);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🏥 ECH Scribe</h1>
        <p>Transform consultation audio into structured assessment data</p>
      </header>

      <div className="container">
        {/* Workflow Steps */}
        <div className="workflow-steps">
          {workflowSteps.filter(step => isStepVisible(step.id)).map((step) => (
            <div
              key={step.id}
              className={`step ${currentStep === step.id ? 'active' : ''} ${
                completedSteps.has(step.id) ? 'completed' : ''
              }`}
              onClick={() => handleStepClick(step.id)}
            >
              <div className="step-number">
                {completedSteps.has(step.id) ? '✓' : step.number}
              </div>
              <div className="step-title">{step.title}</div>
            </div>
          ))}
        </div>

        {/* Main Content */}
        <div className="main-content">
          {currentStep === 'input-choice' && (
            <div className="panel">
              <InputMethodSelector onSelectMethod={handleMethodSelect} />
            </div>
          )}

          {currentStep === 'consent' && (
            <div className="panel">
              <h2>Client Consent</h2>
              <p>Consent form will be implemented here</p>
            </div>
          )}

          {currentStep === 'record' && (
            <div className="panel">
              <h2>
                {selectedMethod === 'live-recording' && 'Record Consultation'}
                {selectedMethod === 'audio-upload' && 'Upload Audio File'}
                {selectedMethod === 'transcript-upload' && 'Upload Transcript'}
              </h2>
              <p>Recording/Upload interface will be implemented here</p>
            </div>
          )}

          {currentStep === 'transcribe' && (
            <div className="panel">
              <h2>Transcribing Audio</h2>
              <p>Transcription progress will be shown here</p>
            </div>
          )}

          {currentStep === 'extract' && (
            <div className="panel">
              <h2>Extracting Clinical Data</h2>
              <p>Extraction progress will be shown here</p>
            </div>
          )}

          {currentStep === 'review' && (
            <div className="panel">
              <h2>Review & Validate Assessment</h2>
              <p>Review interface will be implemented here</p>
            </div>
          )}

          {currentStep === 'submit' && (
            <div className="panel">
              <h2>✅ Assessment Submitted Successfully</h2>
              <p>Submission confirmation will be shown here</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
