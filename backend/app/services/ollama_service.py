"""Ollama LLM service for clinical data extraction"""

import httpx
from typing import Dict, Any, Optional
from app.config import settings


class OllamaService:
    """Service for interacting with Ollama LLM server"""
    
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.timeout = settings.ollama_timeout
    
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Generate text using Ollama
        
        Args:
            prompt: The input prompt
            model: Model name (defaults to configured model)
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            
        Returns:
            Dict containing the generated response
        """
        model_name = model or self.model
        
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature,
            }
        }
        
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            response.raise_for_status()
            return response.json()
    
    async def chat(
        self,
        messages: list[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.1,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Chat completion using Ollama
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (defaults to configured model)
            temperature: Sampling temperature (0.0-1.0)
            stream: Whether to stream the response
            
        Returns:
            Dict containing the chat response
        """
        model_name = model or self.model
        
        payload = {
            "model": model_name,
            "messages": messages,
            "stream": stream,
            "options": {
                "temperature": temperature,
            }
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )
            response.raise_for_status()
            return response.json()
    
    async def extract_clinical_data(
        self,
        transcript: str,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract structured clinical data from transcript using Ollama
        
        Args:
            transcript: The consultation transcript
            model: Model name (defaults to configured model)
            
        Returns:
            Dict containing extracted clinical data in OT Form structure
        """
        prompt = self._build_extraction_prompt(transcript)
        
        response = await self.generate(
            prompt=prompt,
            model=model,
            temperature=0.1,
            max_tokens=4096
        )
        
        # Parse the response and extract JSON
        # Note: This is a simplified version - production would need robust JSON parsing
        return response
    
    def _build_extraction_prompt(self, transcript: str) -> str:
        """Build the prompt for clinical data extraction"""
        return f"""You are a clinical documentation assistant. Extract structured OT assessment data from the following consultation transcript.

TRANSCRIPT:
{transcript}

Extract the following information in JSON format matching the OT Assessment Form structure with 38 fields across 9 categories:

{{
  "client_information": {{
    "client_name": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "dob": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "address": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "phone": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "emergency_contact": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}}
  }},
  "referral_information": {{
    "referral_source": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "referral_date": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "referral_reason": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}}
  }},
  "medical_history": {{
    "diagnosis": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "secondary_conditions": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "medications": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "allergies": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}}
  }},
  "functional_mobility": {{
    "mobility_indoor": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "mobility_outdoor": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "transfers": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "stairs": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "falls_history": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}}
  }},
  "functional_selfcare": {{
    "bathing": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "dressing": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "grooming": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "toileting": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "feeding": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}}
  }},
  "functional_domestic": {{
    "meal_prep": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "housework": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "laundry": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "shopping": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}}
  }},
  "home_environment": {{
    "home_type": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "home_access": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "bathroom_setup": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "home_hazards": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}}
  }},
  "cognitive_psychosocial": {{
    "cognitive_status": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "mood": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "social_support": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}}
  }},
  "goals_plan": {{
    "client_goals": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "assessment_summary": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}},
    "recommendations": {{"value": "", "confidence": 0.0-1.0, "sourceText": ""}}
  }}
}}

Rules:
- Only extract information explicitly stated in the transcript
- Prioritize client and carer statements for subjective data
- Prioritize clinician statements for observations
- Include confidence score (0.0-1.0) for each field
- Include the exact source text that supports each extraction
- Use null for fields not mentioned in the transcript
- Follow OT Assessment Form structure with 38 fields across 9 categories

Return ONLY the JSON object, no additional text."""
    
    async def health_check(self) -> bool:
        """Check if Ollama service is available"""
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception:
            return False


# Global service instance
ollama_service = OllamaService()
