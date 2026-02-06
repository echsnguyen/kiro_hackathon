"""Test health check endpoint"""

import pytest
from httpx import AsyncClient


@pytest.mark.unit
async def test_health_check(client: AsyncClient):
    """Test that health check endpoint returns healthy status"""
    response = await client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data


@pytest.mark.unit
async def test_root_endpoint(client: AsyncClient):
    """Test that root endpoint returns API information"""
    response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


@pytest.mark.unit
async def test_api_root(client: AsyncClient):
    """Test that API v1 root endpoint returns information"""
    response = await client.get("/api/v1/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data
