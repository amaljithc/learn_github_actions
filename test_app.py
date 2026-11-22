"""
Unit Tests for app.py
======================
These tests are automatically run by the CI workflow (01-python-ci.yml).
Run locally with:  pytest test_app.py -v
"""

import pytest
from app import app


@pytest.fixture
def client():
    """Create a Flask test client for each test."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Root endpoint ────────────────────────────────────────────

def test_home(client):
    """GET / should return a welcome JSON message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert data["version"] == "1.0.0"


# ── Health check ─────────────────────────────────────────────

def test_health(client):
    """GET /health should report healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


# ── Addition endpoint ────────────────────────────────────────

def test_add(client):
    """GET /add/2/3 should return 5."""
    response = client.get("/add/2/3")
    assert response.status_code == 200
    assert response.get_json()["result"] == 5


def test_add_negative_numbers(client):
    """Addition should work with negative numbers."""
    response = client.get("/add/-1/1")
    assert response.status_code == 200
    assert response.get_json()["result"] == 0


# ── Multiplication endpoint ──────────────────────────────────

def test_multiply(client):
    """GET /multiply/4/5 should return 20."""
    response = client.get("/multiply/4/5")
    assert response.status_code == 200
    assert response.get_json()["result"] == 20


def test_multiply_by_zero(client):
    """Multiplying by zero should return 0."""
    response = client.get("/multiply/7/0")
    assert response.status_code == 200
    assert response.get_json()["result"] == 0
