from uuid import uuid4

from fastapi.testclient import TestClient
from pymongo.database import Database
import pytest_asyncio
from httpx import Response

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


def test_get_all_user(app_client: TestClient, insert_user_mongo, app_superuser):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    response = app_client.get(url=USER_URL, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[1]['id'] == str(insert_user_mongo['_id'])


def test_get_user(app_client: TestClient, insert_user_mongo, app_superuser):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    url = f"{USER_URL}/{insert_user_mongo['_id']}"
    response = app_client.get(url=url, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert result['id'] == str(insert_user_mongo['_id'])
    assert result['username'] == insert_user_mongo['username']
    assert result['email'] == insert_user_mongo['email']


def test_create_user(app_client: TestClient, app_superuser):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    user_data = {
        "username": "username",
        "password": "pass123",
        "email": "username@username.com",
    }
    user_response = app_client.post(USER_URL, json=user_data, headers=headers)
    assert user_response.status_code == 201
    response_data = user_response.json()
    assert response_data["username"] == user_data["username"]
    assert response_data["email"] == user_data["email"]
    assert response_data["id"] is not None


def test_update_user(app_client: TestClient, insert_user_mongo, app_superuser):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    user_id = str(insert_user_mongo["_id"])
    url = f'{USER_URL}/{user_id}'
    user_data = {
        "username": "fakeuser_updated",
        "password": "pass123",
        "email": "user@username.com",
    }
    user_response = app_client.patch(url=url, json=user_data, headers=headers)
    assert user_response.status_code == 200
    response_data = user_response.json()
    assert response_data["username"] == user_data["username"]
    assert response_data["email"] == user_data["email"]
    assert response_data["id"] is not None


def test_delete_user(app_client: TestClient, insert_user_mongo, app_superuser):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    user_id = str(insert_user_mongo["_id"])
    url = f'{USER_URL}/{user_id}'
    user_response = app_client.delete(url=url, headers=headers)
    assert user_response.status_code == 204


def test_access_token(app_client: TestClient, app_superuser):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    url = f'{USER_URL}/me'
    response: Response = app_client.get(url=url, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert result['username'] == settings.FIRST_SUPERUSER_USERNAME
    assert result['email'] == settings.FIRST_SUPERUSER_EMAIL
