import os

from dotenv import load_dotenv, find_dotenv
import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient

from src.core.config import settings
from src.server import app

env_path = find_dotenv(filename='.env.test')
load_dotenv(env_path)

TEST_DB_URI = os.getenv('TEST_DB_URI')
TEST_DB = os.getenv('TEST_DB')


@pytest.fixture(scope='module')
def mongo_client():
    client = MongoClient(TEST_DB_URI, uuidRepresentation='standard')
    yield client
    client.drop_database(TEST_DB)


@pytest.fixture(scope='module')
def mongo_db(mongo_client: MongoClient):
    db = mongo_client[TEST_DB]
    yield db


@pytest.fixture(scope='module')
def app_client():
    settings.MONGO_DATABASE_URI = TEST_DB_URI
    settings.MONGO_DB = TEST_DB
    with TestClient(app) as client:
        yield client
