from uuid import uuid4

from fastapi.testclient import TestClient

from pymongo.database import Database

import pytest_asyncio

from src.core.config import settings


@pytest_asyncio.fixture
async def insert_user_mongo(mongo_db: Database):
    user = {
        "_id": uuid4(),
        "username": "fakeuser",
        "password": "pass123",
        "email": "fakeuser@username.com",
    }
    mongo_db["User"].insert_one(user)
    yield user


def test_create_user(app_client: TestClient):
    user_url = f'{settings.API_STR}shared/user/'

    user_data = {
        "username": "username",
        "password": "pass123",
        "email": "username@username.com",
    }

    user_response = app_client.post(user_url, json=user_data)

    assert user_response.status_code == 201
    response_data = user_response.json()
    assert response_data["username"] == user_data["username"]
    assert response_data["email"] == user_data["email"]
    assert response_data["id"] is not None


def test_update_user(app_client: TestClient, insert_user_mongo):

    user_id = str(insert_user_mongo["_id"])
    user_url = f'{settings.API_STR}shared/user/{user_id}'

    user_data = {
        "username": "fakeuser_updated",
        "password": "pass123",
        "email": "user@username.com",
    }

    user_response = app_client.patch(user_url, json=user_data)

    assert user_response.status_code == 200
    response_data = user_response.json()
    assert response_data["username"] == user_data["username"]
    assert response_data["email"] == user_data["email"]
    assert response_data["id"] is not None


def test_delete_user(app_client: TestClient, insert_user_mongo):

    user_id = str(insert_user_mongo["_id"])
    user_url = f'{settings.API_STR}shared/user/{user_id}'

    user_response = app_client.delete(user_url)

    assert user_response.status_code == 204
