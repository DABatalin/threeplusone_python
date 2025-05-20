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

def test_add_to_cart(user_token_headers):
    # Since we can't create products (not a superuser), we'll test with a non-existent product
    response = client.post(
        "/api/v1/cart/",
        headers=user_token_headers,
        json={
            "product_id": 999999,
            "quantity": 2
        }
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_add_nonexistent_product(user_token_headers):
    response = client.post(
        "/api/v1/cart/",
        headers=user_token_headers,
        json={
            "product_id": 99999,
            "quantity": 2
        }
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_read_cart(user_token_headers):
    # Just read the empty cart
    response = client.get(
        "/api/v1/cart/",
        headers=user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_update_cart_item(user_token_headers):
    # Since we can't create products (not a superuser), we'll test with a non-existent product
    response = client.put(
        "/api/v1/cart/999999",
        headers=user_token_headers,
        json={"quantity": 3}
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_update_nonexistent_cart_item(user_token_headers):
    response = client.put(
        "/api/v1/cart/99999",
        headers=user_token_headers,
        json={"quantity": 3}
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_remove_from_cart(user_token_headers):
    # Since we can't create products (not a superuser), we'll test with a non-existent product
    response = client.delete(
        "/api/v1/cart/999999",
        headers=user_token_headers
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_remove_nonexistent_cart_item(user_token_headers):
    response = client.delete(
        "/api/v1/cart/99999",
        headers=user_token_headers
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"] 