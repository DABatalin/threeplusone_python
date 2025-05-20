from typing import Dict

from fastapi.testclient import TestClient

def create_test_user(client: TestClient) -> Dict:
    user_data = {
        "email": "test@example.com",
        "password": "test123",
        "full_name": "Test User"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    print(f"Register response status: {response.status_code}")
    print(f"Register response body: {response.json()}")
    if response.status_code != 200:
        raise Exception(f"Failed to create test user: {response.json()}")
    return response.json()

def create_test_superuser(client: TestClient) -> Dict:
    # First create a regular user
    user_data = {
        "email": "admin@example.com",
        "password": "admin123",
        "full_name": "Admin User",
        "is_superuser": True
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    print(f"Register superuser response status: {response.status_code}")
    print(f"Register superuser response body: {response.json()}")
    if response.status_code != 200:
        raise Exception(f"Failed to create superuser: {response.json()}")
    return response.json()

def get_user_token_headers(client: TestClient) -> Dict[str, str]:
    # First create a user
    create_test_user(client)
    
    login_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    print(f"Login response status: {response.status_code}")
    print(f"Login response body: {response.json()}")
    if response.status_code != 200:
        raise Exception(f"Failed to login test user: {response.json()}")
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}

def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    # First create a superuser
    create_test_superuser(client)
    
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    print(f"Login superuser response status: {response.status_code}")
    print(f"Login superuser response body: {response.json()}")
    if response.status_code != 200:
        raise Exception(f"Failed to login superuser: {response.json()}")
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}

def create_test_product(client: TestClient, superuser_token_headers: Dict[str, str]) -> Dict:
    # First create a test seller
    seller_data = {
        "name": "Test Seller",
        "email": "seller@example.com",
        "phone": "+1234567890",
        "address": "123 Test St"
    }
    seller_response = client.post(
        "/api/v1/sellers/",
        headers=superuser_token_headers,
        json=seller_data
    )
    if seller_response.status_code != 200:
        raise Exception(f"Failed to create test seller: {seller_response.json()}")
    seller = seller_response.json()

    # Then create a test product
    product_data = {
        "name": "Test Product",
        "description": "A test product",
        "price": 9.99,
        "seller_id": seller["id"],
        "quantity_available": 100
    }
    response = client.post(
        "/api/v1/products/",
        headers=superuser_token_headers,
        json=product_data
    )
    if response.status_code != 200:
        raise Exception(f"Failed to create test product: {response.json()}")
    return response.json()

def create_test_comment(client: TestClient, user_token_headers: Dict[str, str], product_id: int) -> Dict:
    comment_data = {
        "product_id": product_id,
        "text": "Test comment",
        "rating": 5
    }
    response = client.post(
        "/api/v1/comments/",
        headers=user_token_headers,
        json=comment_data
    )
    if response.status_code != 200:
        raise Exception(f"Failed to create test comment: {response.json()}")
    return response.json() 