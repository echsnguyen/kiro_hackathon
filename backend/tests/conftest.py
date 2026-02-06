"""Pytest configuration and fixtures"""

import asyncio
from typing import AsyncGenerator, Generator
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.database import Base, get_db
from app.config import settings


# Test database URL (use separate test database)
TEST_DATABASE_URL = settings.database_url.replace("/allied_health_db", "/allied_health_test_db")


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an event loop for the test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session"""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with database session override"""
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_audio_file():
    """Fixture for sample audio file data"""
    return {
        "filename": "test_consultation.wav",
        "content_type": "audio/wav",
        "size": 1024 * 1024,  # 1MB
        "duration": 300,  # 5 minutes
    }


@pytest.fixture
def sample_consent_data():
    """Fixture for sample consent data"""
    return {
        "session_id": "test-session-123",
        "consent_method": "digital_signature",
        "clinician_id": "clinician-456",
        "client_id": "client-789",
        "signature_data": "base64-encoded-signature",
    }


@pytest.fixture
def sample_transcript():
    """Fixture for sample transcript data"""
    return {
        "text": "This is a test consultation transcript.",
        "segments": [
            {
                "text": "Hello, how are you feeling today?",
                "start_time": 0.0,
                "end_time": 2.5,
                "confidence": 0.95,
                "speaker": "clinician",
            },
            {
                "text": "I'm feeling okay, just a bit tired.",
                "start_time": 2.5,
                "end_time": 5.0,
                "confidence": 0.92,
                "speaker": "client",
            },
        ],
        "confidence": 0.93,
    }
