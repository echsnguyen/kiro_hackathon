// Demo application logic

let currentStep = 'review';
let validatedFields = new Set();
let highlightedSegmentId = null;
let selectedInputMethod = null;

// Initialize the demo
document.addEventListener('DOMContentLoaded', () => {
    initializeConsent();
    renderTranscript();
    renderForm();
    updateValidationStats();
    showStep(currentStep);
});

// Consent handling
function initializeConsent() {
    const consentCheck = document.getElementById('consent-check');
    const consentBtn = document.getElementById('consent-btn');
    
    consentCheck.addEventListener('change', (e) => {
        consentBtn.disabled = !e.target.checked;
    });
}

// Input method selection
function selectInputMethod(method) {
    selectedInputMethod = method;
    
    // Update UI based on selection
    const recordTitle = document.getElementById('record-title');
    const recordingControls = document.getElementById('recording-controls');
    const uploadAudioControls = document.getElementById('upload-audio-controls');
    const uploadTranscriptControls = document.getElementById('upload-transcript-controls');
    
    // Hide all controls
    recordingControls.style.display = 'none';
    uploadAudioControls.style.display = 'none';
    uploadTranscriptControls.style.display = 'none';
    
    // Show appropriate controls
    if (method === 'record') {
        recordTitle.textContent = 'Record Consultation';
        recordingControls.style.display = 'block';
    } else if (method === 'upload-audio') {
        recordTitle.textContent = 'Upload Audio File';
        uploadAudioControls.style.display = 'block';
    } else if (method === 'upload-transcript') {
        recordTitle.textContent = 'Upload Transcript';
        uploadTranscriptControls.style.display = 'block';
    }
    
    // Mark input-choice step as complete
    document.querySelector('[data-step="input-choice"]').classList.add('completed');
    
    // Navigate to record/upload step
    nextStep('record');
}

// Handle audio file upload
function handleAudioUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const statusDiv = document.getElementById('audio-upload-status');
    statusDiv.innerHTML = `
        <div class="status-message status-info" style="margin-top: 1rem;">
            <strong>Processing audio file: ${file.name}</strong><br>
            Encrypting and uploading... (simulated)
        </div>
    `;
    
    // Simulate upload and processing
    setTimeout(() => {
        statusDiv.innerHTML = `
            <div class="status-message status-success" style="margin-top: 1rem;">
                <strong>Upload complete!</strong><br>
                File encrypted and ready for transcription
            </div>
        `;
        
        // Mark step as complete
        document.querySelector('[data-step="record"]').classList.add('completed');
        
        // Auto-advance to transcription
        setTimeout(() => {
            nextStep('transcribe');
        }, 1500);
    }, 2000);
}

// Handle transcript file upload
function handleTranscriptUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('transcript-text-input').value = e.target.result;
        handleTranscriptText();
    };
    reader.readAsText(file);
}

// Handle transcript text input
function handleTranscriptText() {
    const text = document.getElementById('transcript-text-input').value.trim();
    
    if (!text) {
        alert('Please enter or upload a transcript first.');
        return;
    }
    
    // Show processing message
    const statusDiv = document.createElement('div');
    statusDiv.className = 'status-message status-info';
    statusDiv.style.marginTop = '1rem';
    statusDiv.innerHTML = '<strong>Processing transcript...</strong><br>Parsing and preparing for extraction';
    document.getElementById('upload-transcript-controls').appendChild(statusDiv);
    
    // Simulate processing
    setTimeout(() => {
        statusDiv.className = 'status-message status-success';
        statusDiv.innerHTML = '<strong>Transcript processed!</strong><br>Ready for clinical data extraction';
        
        // Mark steps as complete
        document.querySelector('[data-step="record"]').classList.add('completed');
        document.querySelector('[data-step="transcribe"]').classList.add('completed');
        
        // Skip transcription, go directly to extraction
        setTimeout(() => {
            nextStep('extract');
        }, 1500);
    }, 2000);
}

// Step navigation
function showStep(step) {
    // Hide all content
    document.querySelectorAll('.main-content').forEach(el => {
        el.classList.remove('active');
    });
    
    // Show selected content
    document.getElementById(`${step}-content`).classList.add('active');
    
    // Update step indicators
    document.querySelectorAll('.step').forEach(el => {
        el.classList.remove('active');
    });
    document.querySelector(`[data-step="${step}"]`).classList.add('active');
    
    currentStep = step;
}

function nextStep(step) {
    showStep(step);
    
    // Auto-progress for certain steps
    if (step === 'transcribe') {
        simulateTranscription();
    } else if (step === 'extract') {
        simulateExtraction();
    } else if (step === 'submit') {
        document.getElementById('submit-timestamp').textContent = new Date().toLocaleString();
    }
}

function prevStep(step) {
    showStep(step);
}

// Recording simulation
let isRecording = false;
let recordingTimer = null;

function simulateRecording() {
    const button = document.querySelector('.record-button');
    const text = document.getElementById('record-text');
    const statusMsg = document.querySelector('#record-content .status-message');
    
    if (!isRecording) {
        isRecording = true;
        button.classList.add('recording');
        text.textContent = 'Recording...';
        statusMsg.innerHTML = '<strong>Recording in progress</strong><br>Speak clearly and ensure all participants are audible';
        statusMsg.className = 'status-message status-info';
        
        // Simulate recording for 3 seconds
        recordingTimer = setTimeout(() => {
            stopRecording();
        }, 3000);
    } else {
        stopRecording();
    }
}

function stopRecording() {
    isRecording = false;
    clearTimeout(recordingTimer);
    
    const button = document.querySelector('.record-button');
    const text = document.getElementById('record-text');
    const statusMsg = document.querySelector('#record-content .status-message');
    
    button.classList.remove('recording');
    text.textContent = 'Recording Complete';
    statusMsg.innerHTML = '<strong>Recording saved successfully</strong><br>Audio encrypted and ready for transcription';
    statusMsg.className = 'status-message status-success';
    
    // Mark step as complete
    document.querySelector('[data-step="record"]').classList.add('completed');
    
    // Auto-advance after 1.5 seconds
    setTimeout(() => {
        nextStep('transcribe');
    }, 1500);
}

// Transcription simulation
function simulateTranscription() {
    const progressBar = document.getElementById('transcribe-progress');
    let progress = 0;
    
    const interval = setInterval(() => {
        progress += 5;
        progressBar.style.width = progress + '%';
        
        if (progress >= 100) {
            clearInterval(interval);
            document.querySelector('[data-step="transcribe"]').classList.add('completed');
            setTimeout(() => {
                nextStep('extract');
            }, 500);
        }
    }, 100);
}

// Extraction simulation
function simulateExtraction() {
    const progressBar = document.getElementById('extract-progress');
    let progress = 0;
    
    const interval = setInterval(() => {
        progress += 4;
        progressBar.style.width = progress + '%';
        
        if (progress >= 100) {
            clearInterval(interval);
            document.querySelector('[data-step="extract"]').classList.add('completed');
            setTimeout(() => {
                nextStep('review');
            }, 500);
        }
    }, 120);
}

// Render transcript
function renderTranscript() {
    const container = document.getElementById('transcript-container');
    
    mockTranscript.forEach(segment => {
        const div = document.createElement('div');
        div.className = 'transcript-segment';
        div.dataset.segmentId = segment.id;
        
        const speakerClass = segment.speaker === 'clinician' ? 'clinician' : 
                            segment.speaker === 'client' ? 'client' : 'carer';
        
        const speakerLabel = segment.speaker.charAt(0).toUpperCase() + segment.speaker.slice(1);
        
        div.innerHTML = `
            <div class="speaker-label ${speakerClass}">
                ${speakerLabel}
                <span class="timestamp">${formatTime(segment.startTime)} - ${formatTime(segment.endTime)}</span>
            </div>
            <div class="segment-text">${segment.text}</div>
        `;
        
        div.addEventListener('click', () => highlightSegment(segment.id));
        
        container.appendChild(div);
    });
}

// Render form
function renderForm() {
    const container = document.getElementById('form-container');
    let currentCategory = '';
    
    mockFormFields.forEach(field => {
        // Add category header if new category
        if (field.category !== currentCategory) {
            currentCategory = field.category;
            const header = document.createElement('h4');
            header.className = 'category-header';
            header.style.marginTop = '1.5rem';
            header.style.marginBottom = '1rem';
            header.style.color = '#667eea';
            header.style.borderBottom = '2px solid #e5e7eb';
            header.style.paddingBottom = '0.5rem';
            header.textContent = formatCategory(field.category);
            container.appendChild(header);
        }
        
        const formGroup = document.createElement('div');
        formGroup.className = 'form-group';
        
        const confidenceClass = field.confidence >= 0.8 ? 'confidence-high' :
                               field.confidence >= 0.6 ? 'confidence-medium' : 'confidence-low';
        
        const confidenceText = field.confidence >= 0.8 ? 'High' :
                              field.confidence >= 0.6 ? 'Medium' : 'Low';
        
        // Use textarea for longer fields
        const isLongField = ['assessment_summary', 'recommendations', 'client_goals', 'referral_reason'].includes(field.id);
        const inputElement = isLongField 
            ? `<textarea 
                class="form-input ${field.flagged ? 'flagged' : ''}" 
                data-field-id="${field.id}"
                rows="4"
                style="resize: vertical; min-height: 80px;"
            >${field.value}</textarea>`
            : `<input 
                type="text" 
                class="form-input ${field.flagged ? 'flagged' : ''}" 
                value="${field.value}"
                data-field-id="${field.id}"
            >`;
        
        formGroup.innerHTML = `
            <label class="form-label">
                ${field.label}
                <span class="confidence-badge ${confidenceClass}">${confidenceText} Confidence</span>
                ${field.flagged ? '<span class="confidence-badge confidence-medium">⚠ Review</span>' : ''}
            </label>
            ${inputElement}
            <div class="checkbox-group">
                <input type="checkbox" id="validate-${field.id}" data-field-id="${field.id}">
                <label for="validate-${field.id}">Validated</label>
            </div>
        `;
        
        container.appendChild(formGroup);
        
        // Add event listeners
        const input = formGroup.querySelector('.form-input');
        const checkbox = formGroup.querySelector('input[type="checkbox"]');
        
        input.addEventListener('focus', () => {
            highlightLinkedSegments(field.id);
        });
        
        input.addEventListener('input', () => {
            // Auto-check validation when user edits
            if (!checkbox.checked) {
                checkbox.checked = true;
                handleValidation(field.id, true);
            }
        });
        
        checkbox.addEventListener('change', (e) => {
            handleValidation(field.id, e.target.checked);
        });
    });
}

// Highlight segment
function highlightSegment(segmentId) {
    // Remove previous highlight
    document.querySelectorAll('.transcript-segment').forEach(el => {
        el.classList.remove('highlighted');
    });
    
    // Add new highlight
    const segment = document.querySelector(`[data-segment-id="${segmentId}"]`);
    if (segment) {
        segment.classList.add('highlighted');
        highlightedSegmentId = segmentId;
    }
}

// Highlight linked segments
function highlightLinkedSegments(fieldId) {
    // Remove previous highlights
    document.querySelectorAll('.transcript-segment').forEach(el => {
        el.classList.remove('highlighted');
    });
    
    // Find and highlight linked segments
    mockTranscript.forEach(segment => {
        if (segment.linkedFields.includes(fieldId)) {
            const el = document.querySelector(`[data-segment-id="${segment.id}"]`);
            if (el) {
                el.classList.add('highlighted');
                // Scroll to first highlighted segment
                if (segment.linkedFields[0] === fieldId) {
                    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        }
    });
}

// Handle validation
function handleValidation(fieldId, isChecked) {
    if (isChecked) {
        validatedFields.add(fieldId);
    } else {
        validatedFields.delete(fieldId);
    }
    
    updateValidationStats();
}

// Update validation stats
function updateValidationStats() {
    const totalFields = mockFormFields.length;
    const validated = validatedFields.size;
    const flagged = mockFormFields.filter(f => f.flagged).length;
    
    document.getElementById('total-fields').textContent = totalFields;
    document.getElementById('validated-fields').textContent = validated;
    document.getElementById('flagged-fields').textContent = flagged;
    
    const progress = totalFields > 0 ? (validated / totalFields) * 100 : 0;
    document.getElementById('validation-progress').style.width = progress + '%';
    
    // Enable submit button when all fields validated
    const submitBtn = document.getElementById('submit-btn');
    if (submitBtn) {
        submitBtn.disabled = validated < totalFields;
    }
}

// Format time
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Format category
function formatCategory(category) {
    const categoryMap = {
        'client_information': 'Client Information',
        'referral_information': 'Referral Information',
        'medical_history': 'Medical History',
        'functional_mobility': 'Functional Assessment - Mobility',
        'functional_selfcare': 'Functional Assessment - Self Care',
        'functional_domestic': 'Functional Assessment - Domestic Tasks',
        'home_environment': 'Home Environment',
        'cognitive_psychosocial': 'Cognitive & Psychosocial',
        'goals_plan': 'Goals & Assessment Summary'
    };
    
    return categoryMap[category] || category.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

// Reset demo
function resetDemo() {
    validatedFields.clear();
    highlightedSegmentId = null;
    selectedInputMethod = null;
    
    // Reset all steps
    document.querySelectorAll('.step').forEach(el => {
        el.classList.remove('completed', 'active');
    });
    
    // Reset checkboxes
    document.querySelectorAll('input[type="checkbox"]').forEach(el => {
        el.checked = false;
    });
    
    // Reset consent
    document.getElementById('consent-check').checked = false;
    document.getElementById('consent-btn').disabled = true;
    
    // Reset recording button
    const recordBtn = document.querySelector('.record-button');
    recordBtn.classList.remove('recording');
    document.getElementById('record-text').textContent = 'Start Recording';
    
    // Reset upload controls
    document.getElementById('audio-file-input').value = '';
    document.getElementById('transcript-file-input').value = '';
    document.getElementById('transcript-text-input').value = '';
    document.getElementById('audio-upload-status').innerHTML = '';
    
    // Reset progress bars
    document.getElementById('transcribe-progress').style.width = '0%';
    document.getElementById('extract-progress').style.width = '0%';
    document.getElementById('validation-progress').style.width = '0%';
    
    updateValidationStats();
    showStep('consent');
}

// Allow clicking on workflow steps
document.querySelectorAll('.step').forEach(step => {
    step.addEventListener('click', () => {
        const stepName = step.dataset.step;
        showStep(stepName);
    });
});
