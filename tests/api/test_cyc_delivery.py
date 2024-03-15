from uuid import uuid4

from fastapi.testclient import TestClient
import pytest_asyncio
from pymongo.database import Database

from src.core.config import settings


@pytest_asyncio.fixture
async def insert_deliveries_mongo(mongo_db: Database):
    result = []
    deliveries = [
        {
            "_id": uuid4(),
            "date": "2025-03-08T12:00:00",
            "months": 3,
            "products": [],
            "family_id": uuid4(),
        }
    ]
    for delivery in deliveries:
        mongo_db['Delivery'].insert_one(delivery)
        result.append(delivery)
    yield result


def test_get_deliveries(app_client: TestClient, insert_deliveries_mongo):
    url = f'{settings.API_STR}cyc/delivery/'
    response = app_client.get(url=url)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) == 1
    for item, delivery in zip(result, insert_deliveries_mongo):
        assert item['id'] == str(delivery['_id'])
        assert item['date'] == delivery['date']
        assert item['months'] == delivery['months']
        assert item['family_id'] == str(delivery['family_id'])
        assert item['products'] == delivery['products']
