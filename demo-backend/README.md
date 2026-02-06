# Demo Backend with Synthetic Data

A lightweight FastAPI backend that generates synthetic consultation data for the AI Allied Health Assessment Automator demo.

## Features

- ✅ Generates realistic synthetic consultation transcripts
- ✅ Generates synthetic clinical data with confidence scores
- ✅ Provides REST API endpoints for data generation
- ✅ CORS enabled for frontend integration
- ✅ No database required - all data generated on-demand
- ✅ Uses Faker library for realistic names and data

## Installation

### 1. Create Virtual Environment

```bash
cd demo-backend
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Generate Complete Consultation
```bash
POST http://localhost:8000/api/v1/generate-consultation?num_segments=20
```

Returns:
- Session ID
- Complete transcript with speaker diarization
- Extracted clinical data with confidence scores
- Metadata (duration, counts, flagged fields)

**Example Response:**
```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "timestamp": "2024-01-15T10:30:00",
  "transcript": [
    {
      "id": 1,
      "speaker": "clinician",
      "text": "How are you feeling today?",
      "startTime": 0,
      "endTime": 3.5,
      "linkedFields": []
    }
  ],
  "clinical_data": {
    "name": {
      "value": "Margaret Thompson",
      "confidence": 0.95,
      "flagged": false
    }
  },
  "metadata": {
    "duration_seconds": 120.5,
    "segment_count": 20,
    "field_count": 13,
    "flagged_count": 3
  }
}
```

### 2. Generate Transcript Only
```bash
POST http://localhost:8000/api/v1/generate-transcript?num_segments=20
```

Returns only the transcript with speaker diarization.

### 3. Generate Clinical Data Only
```bash
POST http://localhost:8000/api/v1/generate-clinical-data
```

Returns only the extracted clinical data fields.

### 4. List Consultations
```bash
GET http://localhost:8000/api/v1/consultations?count=5
```

Returns a list of synthetic consultation summaries.

### 5. Health Check
```bash
GET http://localhost:8000/health
```

Returns server health status.

## Testing the API

### Using curl:

```bash
# Generate a complete consultation
curl -X POST "http://localhost:8000/api/v1/generate-consultation?num_segments=20"

# Generate transcript only
curl -X POST "http://localhost:8000/api/v1/generate-transcript?num_segments=15"

# Generate clinical data only
curl -X POST "http://localhost:8000/api/v1/generate-clinical-data"

# List consultations
curl "http://localhost:8000/api/v1/consultations?count=5"
```

### Using Python:

```python
import requests

# Generate consultation
response = requests.post("http://localhost:8000/api/v1/generate-consultation?num_segments=20")
data = response.json()

print(f"Session ID: {data['session_id']}")
print(f"Transcript segments: {data['metadata']['segment_count']}")
print(f"Flagged fields: {data['metadata']['flagged_count']}")
```

### Using the Interactive Docs:

Open http://localhost:8000/docs in your browser to use the interactive Swagger UI.

## Synthetic Data Details

### Transcript Generation
- Alternates between clinician and client speakers
- Realistic medical consultation dialogue
- Random timing and duration for each segment
- 15-25 segments per consultation (configurable)

### Clinical Data Fields
- **Demographics**: name, age, living arrangements
- **Clinical History**: medications, surgeries, chronic conditions
- **Functional Status**: mobility, falls history, ADLs
- **Goals**: client goals and aspirations
- **Risk Assessment**: cognitive state, skin integrity, nutrition

### Confidence Scores
- High confidence: 0.80-0.99
- Medium confidence: 0.60-0.79
- Low confidence: 0.50-0.69
- Fields with confidence < 0.70 are automatically flagged for review

## Integrating with Frontend

Update your frontend to call the API:

```javascript
// Fetch synthetic consultation data
async function loadConsultation() {
    const response = await fetch('http://localhost:8000/api/v1/generate-consultation?num_segments=20', {
        method: 'POST'
    });
    const data = await response.json();
    
    // Use the data in your UI
    renderTranscript(data.transcript);
    renderClinicalData(data.clinical_data);
}
```

## Environment Variables

Create a `.env` file (optional):

```bash
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
```

## Production Notes

⚠️ **This is a demo backend only!**

For production use, you would need:
- Real database (PostgreSQL)
- Authentication and authorization
- Actual AI/ML services (Whisper, Gemini)
- Encryption at rest and in transit
- Audit logging
- Rate limiting
- Error handling and validation

See the main project for the full production implementation.

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

### CORS Issues
The API has CORS enabled for all origins (`allow_origins=["*"]`). For production, restrict this to specific domains.

### Import Errors
Make sure you've activated the virtual environment and installed all dependencies:
```bash
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Next Steps

1. Start the backend: `python main.py`
2. Test the API: Open http://localhost:8000/docs
3. Generate data: Use the `/generate-consultation` endpoint
4. Integrate with frontend: Update demo to fetch from API
5. Explore the data: Try different parameters and endpoints

Enjoy your synthetic data! 🎉
