"""Application configuration using pydantic-settings"""

from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = "AI Allied Health Assessment Automator"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    secret_key: str = Field(..., min_length=32)
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False
    
    # Database
    database_url: str = Field(..., description="PostgreSQL connection URL")
    database_pool_size: int = 20
    database_max_overflow: int = 10
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    
    # AWS S3
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    aws_s3_bucket: str = ""
    aws_s3_encryption: str = "AES256"
    
    # Azure Blob Storage
    azure_storage_connection_string: str = ""
    azure_storage_container: str = ""
    
    # Encryption
    encryption_key: str = Field(..., description="Base64 encoded encryption key")
    encryption_algorithm: str = "AES-256-GCM"
    
    # Authentication
    jwt_secret_key: str = Field(..., min_length=32)
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    
    # OAuth 2.0
    oauth_provider: str = "auth0"
    oauth_domain: str = ""
    oauth_client_id: str = ""
    oauth_client_secret: str = ""
    oauth_audience: str = ""
    
    # AI Services
    whisper_model: str = "large-v3"
    whisper_device: str = "cpu"
    whisper_api_url: str = ""
    
    google_api_key: str = ""
    gemini_model: str = "gemini-1.5-pro"
    gemini_temperature: float = 0.1
    gemini_max_tokens: int = 8192
    
    pyannote_auth_token: str = ""
    pyannote_model: str = "pyannote/speaker-diarization-3.1"
    
    # Portal Integration
    portal_api_url: str = ""
    portal_api_key: str = ""
    portal_api_timeout: int = 30
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    log_file: str = "logs/app.log"
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    cors_allow_credentials: bool = True
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    rate_limit_burst: int = 10
    
    # File Upload
    max_upload_size_mb: int = 500
    allowed_audio_formats: str = "wav,mp3,m4a,flac,ogg"
    
    # Processing
    transcription_timeout_seconds: int = 300
    extraction_timeout_seconds: int = 120
    diarization_timeout_seconds: int = 180
    
    # Compliance
    pii_redaction_enabled: bool = False
    audit_log_retention_days: int = 2555  # 7 years
    data_retention_policy: str = "zero"
    
    @field_validator("cors_origins")
    @classmethod
    def parse_cors_origins(cls, v: str) -> List[str]:
        """Parse comma-separated CORS origins"""
        return [origin.strip() for origin in v.split(",")]
    
    @field_validator("allowed_audio_formats")
    @classmethod
    def parse_audio_formats(cls, v: str) -> List[str]:
        """Parse comma-separated audio formats"""
        return [fmt.strip() for fmt in v.split(",")]
    
    @property
    def max_upload_size_bytes(self) -> int:
        """Convert max upload size from MB to bytes"""
        return self.max_upload_size_mb * 1024 * 1024


# Global settings instance
settings = Settings()
