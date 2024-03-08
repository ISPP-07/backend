import os

from dotenv import load_dotenv, find_dotenv
import pytest
from fastapi.testclient import TestClient

from src.core.config import settings
from src.main import app

env_path = find_dotenv(filename='.env.test')
load_dotenv(env_path)

TEST_DB_URI = os.getenv('TEST_DB_URI')
TEST_DB = os.getenv('TEST_DB')


@pytest.fixture(scope='session')
def app_client():
    settings.MONGO_DATABASE_URI = 'mongodb://isppuser:ispp123@localhost:27017/'
    settings.MONGO_DB = 'ispptest'
    with TestClient(app) as client:
        yield client
