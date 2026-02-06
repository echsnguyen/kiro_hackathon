"""Demo Backend API with Synthetic Data Generation"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from faker import Faker
import random
from datetime import datetime
from typing import List, Dict, Any

app = FastAPI(
    title="AI Allied Health Assessment Automator - Demo API",
    version="1.0.0",
    description="Demo backend with synthetic data generation"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fake = Faker()

# Synthetic data generators
def generate_transcript_segment(segment_id: int, speaker: str, start_time: float) -> Dict[str, Any]:
    """Generate a synthetic transcript segment"""
    templates = {
        "clinician": [
            "How are you feeling today?",
            "Can you tell me more about that?",
            "Have you had any falls recently?",
            "What medications are you currently taking?",
            "How are you managing with daily activities?",
            "What are your goals for your health?",
        ],
        "client": [
            f"I'm {random.randint(65, 90)} years old and I live {random.choice(['alone', 'with my spouse', 'with family'])}.",
            f"I've been having trouble with {random.choice(['mobility', 'balance', 'stairs', 'walking'])}.",
            f"I take {random.choice(['blood pressure medication', 'cholesterol medication', 'diabetes medication'])}.",
            f"I had {random.choice(['hip replacement', 'knee surgery', 'heart surgery'])} {random.randint(1, 10)} years ago.",
            f"I have {random.choice(['arthritis', 'diabetes', 'high blood pressure', 'heart disease'])}.",
            f"I want to be able to {random.choice(['walk to the shops', 'visit family', 'garden', 'travel'])} again.",
        ]
    }
    
    text = random.choice(templates.get(speaker, ["..."]))
    duration = random.uniform(3, 8)
    
    return {
        "id": segment_id,
        "speaker": speaker,
        "text": text,
        "startTime": start_time,
        "endTime": start_time + duration,
        "linkedFields": []
    }

def generate_consultation_transcript(num_segments: int = 20) -> List[Dict[str, Any]]:
    """Generate a complete synthetic consultation transcript"""
    segments = []
    current_time = 0
    
    for i in range(num_segments):
        speaker = "clinician" if i % 2 == 0 else "client"
        segment = generate_transcript_segment(i + 1, speaker, current_time)
        segments.append(segment)
        current_time = segment["endTime"] + random.uniform(0.5, 2)
    
    return segments

def generate_clinical_data() -> Dict[str, Any]:
    """Generate synthetic clinical data"""
    age = random.randint(65, 90)
    
    return {
        "name": {
            "value": fake.name(),
            "confidence": round(random.uniform(0.85, 0.99), 2),
            "flagged": False
        },
        "age": {
            "value": str(age),
            "confidence": round(random.uniform(0.90, 0.99), 2),
            "flagged": False
        },
        "living_arrangements": {
            "value": random.choice([
                "Lives alone in apartment",
                "Lives with spouse",
                "Lives with family",
                "Assisted living facility"
            ]),
            "confidence": round(random.uniform(0.80, 0.95), 2),
            "flagged": False
        },
        "current_medications": {
            "value": ", ".join(random.sample([
                "Lisinopril (blood pressure)",
                "Atorvastatin (cholesterol)",
                "Metformin (diabetes)",
                "Aspirin",
                "Vitamin D supplements",
                "Calcium supplements"
            ], k=random.randint(2, 4))),
            "confidence": round(random.uniform(0.75, 0.92), 2),
            "flagged": random.random() < 0.2
        },
        "past_surgeries": {
            "value": random.choice([
                "Hip replacement (left side, 5 years ago)",
                "Knee replacement (right side, 3 years ago)",
                "Cataract surgery (both eyes)",
                "Appendectomy (20 years ago)",
                "No major surgeries"
            ]),
            "confidence": round(random.uniform(0.85, 0.96), 2),
            "flagged": False
        },
        "chronic_conditions": {
            "value": ", ".join(random.sample([
                "Hypertension",
                "Type 2 Diabetes",
                "Osteoarthritis",
                "Hypercholesterolemia",
                "Chronic kidney disease (stage 2)"
            ], k=random.randint(2, 3))),
            "confidence": round(random.uniform(0.80, 0.94), 2),
            "flagged": False
        },
        "mobility": {
            "value": random.choice([
                "Decreased mobility, uses walking stick",
                "Difficulty with stairs, uses handrail",
                "Walks slowly, tires easily",
                "Uses walker for outdoor activities"
            ]),
            "confidence": round(random.uniform(0.55, 0.75), 2),
            "flagged": True
        },
        "falls_history": {
            "value": random.choice([
                "One fall in bathroom 2 weeks ago, minor bruising",
                "Two falls in past 6 months, no injuries",
                "No recent falls",
                "Fall 3 months ago, fractured wrist"
            ]),
            "confidence": round(random.uniform(0.80, 0.93), 2),
            "flagged": False
        },
        "adls": {
            "value": random.choice([
                "Can dress self (slower), difficulty with meal preparation",
                "Independent with most ADLs, needs help with bathing",
                "Difficulty with buttons and zippers, uses adaptive equipment",
                "Needs assistance with cooking and cleaning"
            ]),
            "confidence": round(random.uniform(0.58, 0.72), 2),
            "flagged": True
        },
        "goals": {
            "value": random.choice([
                "Walk to local shops independently, visit family more often",
                "Improve balance and reduce fall risk",
                "Return to gardening activities",
                "Travel to see grandchildren interstate"
            ]),
            "confidence": round(random.uniform(0.85, 0.96), 2),
            "flagged": False
        },
        "cognitive_state": {
            "value": random.choice([
                "Memory intact, occasional minor forgetfulness",
                "Mild cognitive impairment, forgets appointments",
                "Alert and oriented, no concerns",
                "Some difficulty with complex tasks"
            ]),
            "confidence": round(random.uniform(0.78, 0.91), 2),
            "flagged": False
        },
        "skin_integrity": {
            "value": random.choice([
                "No pressure sores or wounds",
                "Dry skin on lower legs, no breaks",
                "Small pressure area on heel (stage 1)",
                "Skin intact, good condition"
            ]),
            "confidence": round(random.uniform(0.88, 0.97), 2),
            "flagged": False
        },
        "nutritional_risks": {
            "value": random.choice([
                "Recent weight loss (5-6 lbs), reduced appetite",
                "Adequate nutrition, maintains weight",
                "Poor dentition affecting food choices",
                "Difficulty swallowing, modified diet"
            ]),
            "confidence": round(random.uniform(0.52, 0.68), 2),
            "flagged": True
        }
    }

# API Endpoints

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "AI Allied Health Assessment Automator - Demo API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "generate_consultation": "/api/v1/generate-consultation",
            "generate_transcript": "/api/v1/generate-transcript",
            "generate_clinical_data": "/api/v1/generate-clinical-data"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/v1/generate-consultation")
def generate_consultation(num_segments: int = 20):
    """Generate a complete synthetic consultation with transcript and clinical data"""
    transcript = generate_consultation_transcript(num_segments)
    clinical_data = generate_clinical_data()
    
    return {
        "session_id": fake.uuid4(),
        "timestamp": datetime.utcnow().isoformat(),
        "transcript": transcript,
        "clinical_data": clinical_data,
        "metadata": {
            "duration_seconds": transcript[-1]["endTime"] if transcript else 0,
            "segment_count": len(transcript),
            "field_count": len(clinical_data),
            "flagged_count": sum(1 for field in clinical_data.values() if field.get("flagged", False))
        }
    }

@app.post("/api/v1/generate-transcript")
def generate_transcript(num_segments: int = 20):
    """Generate only a synthetic transcript"""
    transcript = generate_consultation_transcript(num_segments)
    
    return {
        "session_id": fake.uuid4(),
        "timestamp": datetime.utcnow().isoformat(),
        "transcript": transcript,
        "metadata": {
            "duration_seconds": transcript[-1]["endTime"] if transcript else 0,
            "segment_count": len(transcript)
        }
    }

@app.post("/api/v1/generate-clinical-data")
def generate_clinical_data_endpoint():
    """Generate only synthetic clinical data"""
    clinical_data = generate_clinical_data()
    
    return {
        "session_id": fake.uuid4(),
        "timestamp": datetime.utcnow().isoformat(),
        "clinical_data": clinical_data,
        "metadata": {
            "field_count": len(clinical_data),
            "flagged_count": sum(1 for field in clinical_data.values() if field.get("flagged", False))
        }
    }

@app.get("/api/v1/consultations")
def list_consultations(count: int = 5):
    """Generate multiple synthetic consultations"""
    consultations = []
    
    for _ in range(count):
        transcript = generate_consultation_transcript(random.randint(15, 25))
        clinical_data = generate_clinical_data()
        
        consultations.append({
            "session_id": fake.uuid4(),
            "timestamp": fake.date_time_this_month().isoformat(),
            "client_name": clinical_data["name"]["value"],
            "client_age": clinical_data["age"]["value"],
            "status": random.choice(["draft", "validated", "submitted"]),
            "flagged_count": sum(1 for field in clinical_data.values() if field.get("flagged", False))
        })
    
    return {
        "consultations": consultations,
        "total": len(consultations)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
