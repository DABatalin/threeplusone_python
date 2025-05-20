import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.api.deps import get_db
from app.tests.deps import get_test_db, init_test_db
from app.tests.utils import (
    create_test_user,
    get_user_token_headers
)

# Override the dependencies
app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    await init_test_db()
    yield

@pytest.fixture
def user_token_headers(setup_db):
    return get_user_token_headers(client)

def test_read_comments_for_nonexistent_product():
    """Test reading comments for a product that doesn't exist"""
    response = client.get("/api/v1/comments/product/999999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_create_comment_unauthorized():
    """Test creating a comment without authentication"""
    response = client.post(
        "/api/v1/comments/",
        json={
            "product_id": 1,
            "text": "Great product!",
            "rating": 5
        }
    )
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

def test_create_comment_nonexistent_product(user_token_headers):
    """Test creating a comment for a product that doesn't exist"""
    response = client.post(
        "/api/v1/comments/",
        headers=user_token_headers,
        json={
            "product_id": 999999,
            "text": "Great product!",
            "rating": 5
        }
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_create_comment_invalid_rating(user_token_headers):
    """Test creating a comment with invalid rating"""
    response = client.post(
        "/api/v1/comments/",
        headers=user_token_headers,
        json={
            "product_id": 1,
            "text": "Great product!",
            "rating": 6  # Rating should be between 1 and 5
        }
    )
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["loc"] == ["body", "rating"] for error in errors)

def test_create_comment_missing_text(user_token_headers):
    """Test creating a comment with missing required text field"""
    response = client.post(
        "/api/v1/comments/",
        headers=user_token_headers,
        json={
            "product_id": 1,
            "rating": 5
        }
    )
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["loc"] == ["body", "text"] for error in errors)

def test_delete_nonexistent_comment(user_token_headers):
    """Test deleting a comment that doesn't exist"""
    response = client.delete(
        "/api/v1/comments/999999",
        headers=user_token_headers
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"] 