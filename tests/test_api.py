"""
Tests for the FastAPI API endpoints.
"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    import os
    os.environ.setdefault("IBM_API_KEY", "test-key")
    os.environ.setdefault("IBM_PROJECT_ID", "test-project")
    os.environ.setdefault("IBM_URL", "https://us-south.ml.cloud.ibm.com")

    from backend.main import app
    return TestClient(app)


def test_health_endpoint(client):
    """Test /api/health returns valid response."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "ibm_status" in data
    assert "index_ready" in data
    assert "doc_count" in data
    gen_model = data["gen_model"]
    embed_model = data["embed_model"]
    assert gen_model in ("meta-llama/llama-3-3-70b-instruct", "demo-cached", "demo-fallback")
    assert embed_model in ("intfloat/multilingual-e5-large", "none")


def test_landing_page(client):
    """Test / returns the landing page."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_agent_page(client):
    """Test /agent returns the agent page."""
    response = client.get("/agent")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_dashboard_page(client):
    """Test /dashboard returns the dashboard page."""
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_health_response_model(client):
    """Test /api/health response matches HealthResponse schema."""
    response = client.get("/api/health")
    data = response.json()
    required_fields = ["status", "ibm_status", "index_ready", "doc_count",
                       "gen_model", "embed_model", "chroma_path"]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"
