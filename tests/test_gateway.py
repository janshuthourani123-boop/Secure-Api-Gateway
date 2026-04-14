import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/gateway/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_protected_route_unauthorized():
    response = client.get("/api/protected")
    assert response.status_code == 401

def test_login_and_access_protected():
    login_response = client.post("/auth/login", data={"username": "user", "password": "user123"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    protected_response = client.get("/api/protected", headers={"Authorization": f"Bearer {token}"})
    assert protected_response.status_code == 200
    assert "Hello user" in protected_response.json()["msg"]

def test_rate_limiter_blocks():
    # Login endpoint allows 10/min. Hitting it 11 times from the same client
    for _ in range(10):
        client.post("/auth/login", data={"username": "wrong", "password": "user123"})
    
    # 11th should be rate limited
    response = client.post("/auth/login", data={"username": "wrong", "password": "user123"})
    assert response.status_code == 429
