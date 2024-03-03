import pytest
from fastapi.testclient import TestClient
from src.core.config import settings


@pytest.mark.asyncio
async def test_create_warehouse_and_product(client: TestClient):
    user_url = f'{settings.API_STR}shared/user/'

    user_data = {
        "username": "username",
        "password": "pass123",
        "email": "username@username.com",
    }

    user_response = client.post(user_url, json=user_data)

    assert user_response.status_code == 201
    response_data = user_response.json()
    assert response_data["username"] == user_data["username"]
    assert response_data["email"] == user_data["email"]
    assert response_data["id"] is not None