from uuid import uuid4
from httpx import Response

from fastapi.testclient import TestClient
from pymongo.database import Database
import pytest

from src.core.config import settings
from src.core.utils.security import get_hashed_password

URL_AUTH = f'{settings.API_STR}shared/auth/'


@pytest.fixture(scope='module')
def create_user_auth(mongo_db: Database):
    password = 'pass123'
    user = {
        '_id': uuid4(),
        'username': 'Pepe',
        'password': get_hashed_password(password),
        'email': 'pepe@test.com',
        'master': False,
    }
    mongo_db['User'].insert_one(user)
    yield {
        'id': str(user['_id']),
        'username': user['username'],
        'hashed_password': user['password'],
        'password': password,
        'email': user['email'],
        'master': user['master'],
    }


@pytest.fixture
def login_user(app_client: TestClient, create_user_auth):
    url = f'{URL_AUTH}login/'
    data = {
        'username': create_user_auth['username'],
        'password': create_user_auth['password']
    }
    response: Response = app_client.post(url=url, data=data)
    result: dict = response.json()
    yield result


@pytest.mark.dependency()
def test_login(app_client: TestClient, create_user_auth):
    url = f'{URL_AUTH}login/'
    data = {
        'username': create_user_auth['username'],
        'password': create_user_auth['password']
    }
    response: Response = app_client.post(url=url, data=data)
    assert response.status_code == 200
    result = response.json()
    assert 'access_token' in result
    assert 'refresh_token' in result


@pytest.mark.dependency(depends=['test_login'])
def test_refresh_token(app_client: TestClient, login_user):
    refresh_token = login_user['refresh_token']
    body = {'refresh_token': refresh_token}
    url = f'{URL_AUTH}refresh/'
    response: Response = app_client.post(url=url, json=body)
    assert response.status_code == 200
    result = response.json()
    assert 'access_token' in result
    assert 'refresh_token' in result


@pytest.mark.dependency(depends=['test_login'])
def test_access_token(app_client: TestClient, login_user, create_user_auth):
    access_token = login_user['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    url = f'{URL_AUTH}test-token/'
    response: Response = app_client.post(url=url, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert result['id'] == create_user_auth['id']
    assert result['username'] == create_user_auth['username']
    assert result['email'] == create_user_auth['email']


@pytest.mark.dependency(depends=['test_login'])
def test_get_secret_and_qr(
        app_client: TestClient,
        login_user,
        create_user_auth):
    access_token = login_user['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    url = f'{URL_AUTH}recovery-qr-code/'
    data = {'email': create_user_auth['email']}
    response: Response = app_client.post(url=url, json=data, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert 'qr_code' in result
    assert 'email' in result
    assert result['email'] == create_user_auth['email']
