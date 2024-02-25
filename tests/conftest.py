import os
from fastapi.testclient import TestClient

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from dotenv import load_dotenv, find_dotenv

from src.core.database.base_crud import Base
from src.core.deps import get_db

from src.main import app

env_path = find_dotenv(filename='.env.test')
load_dotenv(env_path)

TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL')


@pytest_asyncio.fixture(scope="session")
async def engine() -> AsyncEngine:
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def connection(engine: AsyncEngine):
    async with engine.connect() as conn:
        trans = await conn.begin()
        yield conn
        await trans.rollback()


@pytest_asyncio.fixture
async def session(connection):
    async_session_local = sessionmaker(
        bind=connection, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_local() as session:
        yield session


@pytest_asyncio.fixture
def override_get_db(session):
    async def _override_get_db():
        yield session
    return _override_get_db


@pytest_asyncio.fixture
def client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
