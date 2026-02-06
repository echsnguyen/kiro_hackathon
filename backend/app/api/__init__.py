"""API routes module"""

from fastapi import APIRouter
from app.api.routes import auth

# Create main API router
api_router = APIRouter()

# Include authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Import and include sub-routers here as they are implemented
# Example:
# from app.api.routes import audio, consent, transcription
# api_router.include_router(audio.router, prefix="/audio", tags=["audio"])
# api_router.include_router(consent.router, prefix="/consent", tags=["consent"])
# api_router.include_router(transcription.router, prefix="/transcription", tags=["transcription"])


@api_router.get("/")
async def api_root():
    """API root endpoint"""
    return {
        "message": "AI Allied Health Assessment Automator API v1",
        "endpoints": {
            "health": "/health",
            "docs": "/api/docs",
            "auth": "/api/v1/auth",
        }
    }
