from uuid import uuid4

from fastapi.testclient import TestClient
import pytest_asyncio
from pymongo.database import Database

from src.core.config import settings


@pytest_asyncio.fixture
async def insert_deliveries_mongo(mongo_db: Database):
    result = []
    product = {
        "id": uuid4(),
        "name": "Pepe",
        "quantity": 1,
        "exp_date": "2025-03-08",
    }

    mongo_db['Product'].insert_one(product)

    deliveries = [
        {
            "_id": uuid4(),
            "date": "2025-03-08",
            "months": 1,
            "products": [product],
            "family_id": uuid4(),
        },
        {
            "_id": uuid4(),
            "date": "2025-03-08",
            "months": 2,
            "products": [product],
            "family_id": uuid4(),
        },
    ]

    for delivery in deliveries:
        mongo_db['Delivery'].insert_one(delivery)
        result.append(delivery)
    yield result


def test_get_delivery_detail(
        app_client: TestClient,
        insert_deliveries_mongo):
    delivery_id = str(insert_deliveries_mongo[0]["_id"])
    url = f'{settings.API_STR}cyc/delivery/{delivery_id}'
    response = app_client.get(url=url)
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == delivery_id
    assert result["months"] == 1
    assert result["products"][0]["id"] == str(
        insert_deliveries_mongo[0]["products"][0]["id"])
    assert result["products"][0]["name"] == "Pepe"
    assert result["products"][0]["quantity"] == 1
    assert result["products"][0]["exp_date"] == "2025-03-08"
    assert result["family_id"] == str(
        insert_deliveries_mongo[0]["family_id"])
    assert result["date"] == "2025-03-08T00:00:00"