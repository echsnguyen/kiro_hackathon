import type { InputMethod } from '../types';
import './InputMethodSelector.css';

interface InputMethodSelectorProps {
  onSelectMethod: (method: InputMethod) => void;
}

export default function InputMethodSelector({ onSelectMethod }: InputMethodSelectorProps) {
  return (
    <div className="input-method-selector">
      <h2>Choose Input Method</h2>
      <p className="subtitle">How would you like to provide the consultation data?</p>
      
      <div className="method-grid">
        <div className="method-card" onClick={() => onSelectMethod('live-recording')}>
          <div className="method-icon">🎤</div>
          <h3>Record Audio</h3>
          <p>Record the consultation in real-time using your device microphone</p>
          <div className="method-features">
            <div className="feature">✓ Live recording</div>
            <div className="feature">✓ Real-time transcription</div>
            <div className="feature">✓ Speaker diarization</div>
            <div className="feature warning">⚠ Requires consent</div>
          </div>
        </div>
        
        <div className="method-card" onClick={() => onSelectMethod('audio-upload')}>
          <div className="method-icon">📁</div>
          <h3>Upload Audio File</h3>
          <p>Upload a pre-recorded audio file from your consultation</p>
          <div className="method-features">
            <div className="feature">✓ Supports MP3, WAV, M4A</div>
            <div className="feature">✓ Automatic transcription</div>
            <div className="feature">✓ Speaker diarization</div>
            <div className="feature">✓ No consent needed</div>
          </div>
        </div>
        
        <div className="method-card" onClick={() => onSelectMethod('transcript-upload')}>
          <div className="method-icon">📄</div>
          <h3>Upload Transcript</h3>
          <p>Upload an existing transcript if you already have one</p>
          <div className="method-features">
            <div className="feature">✓ Skip transcription</div>
            <div className="feature">✓ Fastest processing</div>
            <div className="feature">✓ Direct to extraction</div>
            <div className="feature">✓ No consent needed</div>
          </div>
        </div>
      </div>
    </div>
  );
}
