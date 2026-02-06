"""Test script for the demo backend API"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_generate_consultation():
    """Test consultation generation"""
    print("Testing consultation generation...")
    response = requests.post(f"{BASE_URL}/api/v1/generate-consultation?num_segments=10")
    print(f"Status: {response.status_code}")
    data = response.json()
    
    print(f"Session ID: {data['session_id']}")
    print(f"Transcript segments: {data['metadata']['segment_count']}")
    print(f"Clinical fields: {data['metadata']['field_count']}")
    print(f"Flagged fields: {data['metadata']['flagged_count']}")
    print(f"\nFirst transcript segment:")
    print(json.dumps(data['transcript'][0], indent=2))
    print(f"\nSample clinical data (name):")
    print(json.dumps(data['clinical_data']['name'], indent=2))
    print()

def test_generate_transcript():
    """Test transcript generation"""
    print("Testing transcript generation...")
    response = requests.post(f"{BASE_URL}/api/v1/generate-transcript?num_segments=5")
    print(f"Status: {response.status_code}")
    data = response.json()
    
    print(f"Session ID: {data['session_id']}")
    print(f"Segments: {data['metadata']['segment_count']}")
    print(f"Duration: {data['metadata']['duration_seconds']:.1f} seconds\n")

def test_generate_clinical_data():
    """Test clinical data generation"""
    print("Testing clinical data generation...")
    response = requests.post(f"{BASE_URL}/api/v1/generate-clinical-data")
    print(f"Status: {response.status_code}")
    data = response.json()
    
    print(f"Session ID: {data['session_id']}")
    print(f"Fields: {data['metadata']['field_count']}")
    print(f"Flagged: {data['metadata']['flagged_count']}\n")

def test_list_consultations():
    """Test consultation listing"""
    print("Testing consultation listing...")
    response = requests.get(f"{BASE_URL}/api/v1/consultations?count=3")
    print(f"Status: {response.status_code}")
    data = response.json()
    
    print(f"Total consultations: {data['total']}")
    print("\nConsultations:")
    for consultation in data['consultations']:
        print(f"  - {consultation['client_name']} (Age {consultation['client_age']}) - Status: {consultation['status']}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("Demo Backend API Test Suite")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_generate_consultation()
        test_generate_transcript()
        test_generate_clinical_data()
        test_list_consultations()
        
        print("=" * 60)
        print("All tests completed successfully! ✅")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API.")
        print("Make sure the server is running: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")
