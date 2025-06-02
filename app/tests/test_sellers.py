import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.api.deps import get_db
from app.tests.deps import get_test_db, init_test_db

# Override the dependencies
app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    await init_test_db()
    yield

def test_read_sellers():
    response = client.get("/api/v1/sellers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_non_existent_seller():
    response = client.get("/api/v1/sellers/999999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"] 