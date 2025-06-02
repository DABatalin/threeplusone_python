import pytest
from fastapi.testclient import TestClient
import pytest_asyncio

from app.main import app
from app.api.deps import get_db
from app.tests.deps import get_test_db, init_test_db

app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    await init_test_db()
    yield

def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data

def test_register_existing_user():
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        }
    )

    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_login_user():
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login_test@example.com",
            "password": "testpassword123",
            "full_name": "Login Test User"
        }
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login_test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_login_wrong_password():
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login_test@example.com",
            "password": "testpassword123",
            "full_name": "Login Test User"
        }
    )
    
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login_test@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 400
    assert "Incorrect email or password" in response.json()["detail"]

def test_login_nonexistent_user():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 400
    assert "Incorrect email or password" in response.json()["detail"]

def test_logout():
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out" 