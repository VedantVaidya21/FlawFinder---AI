import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "Welcome to FlawFinder AI" in response.json().get("message", "")

@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json().get("status") == "healthy"

@pytest.mark.asyncio
async def test_ping_db_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/ping-db")
    assert response.status_code == 200
    json_resp = response.json()
    assert "status" in json_resp
    assert json_resp["status"] in ["connected", "error"]

# Additional tests for flows endpoints would require authentication and setup
# These are placeholders for further tests once auth is implemented
