from uuid import uuid4

from fastapi.testclient import TestClient

from pymongo.database import Database

import pytest_asyncio

from src.core.config import settings

USER_URL = f'{settings.API_STR}shared/user'


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


def test_get_all_user(app_client: TestClient, insert_user_mongo):
    response = app_client.get(url=USER_URL)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['id'] == str(insert_user_mongo['_id'])


def test_get_user(app_client: TestClient, insert_user_mongo):
    url = f'{USER_URL}/{insert_user_mongo['_id']}'
    response = app_client.get(url=url)
    assert response.status_code == 200
    result = response.json()
    assert result['id'] == str(insert_user_mongo['_id'])
    assert result['username'] == insert_user_mongo['username']
    assert result['email'] == insert_user_mongo['email']


def test_create_user(app_client: TestClient):
    user_data = {
        "username": "username",
        "password": "pass123",
        "email": "username@username.com",
    }
    user_response = app_client.post(USER_URL, json=user_data)
    assert user_response.status_code == 201
    response_data = user_response.json()
    assert response_data["username"] == user_data["username"]
    assert response_data["email"] == user_data["email"]
    assert response_data["id"] is not None


def test_update_user(app_client: TestClient, insert_user_mongo):

    user_id = str(insert_user_mongo["_id"])
    url = f'{USER_URL}/{user_id}'

    user_data = {
        "username": "fakeuser_updated",
        "password": "pass123",
        "email": "user@username.com",
    }

    user_response = app_client.patch(url=url, json=user_data)

    assert user_response.status_code == 200
    response_data = user_response.json()
    assert response_data["username"] == user_data["username"]
    assert response_data["email"] == user_data["email"]
    assert response_data["id"] is not None


def test_delete_user(app_client: TestClient, insert_user_mongo):

    user_id = str(insert_user_mongo["_id"])
    url = f'{USER_URL}/{user_id}'

    user_response = app_client.delete(url=url)

    assert user_response.status_code == 204
