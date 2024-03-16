from uuid import uuid4

from fastapi.testclient import TestClient
import pytest_asyncio
from pymongo.database import Database

from src.core.config import settings


@pytest_asyncio.fixture
async def insert_warehouse_mongo(mongo_db: Database):
    warehouse = {
        "_id": uuid4(),
        "name": "Almacén principal",
        "products": [
            {
                "id": uuid4(),
                "name": "Leche desnatada",
                "quantity": 34,
                "exp_date": "2025-03-16"
            }
        ]
    }

    mongo_db['Warehouse'].insert_one(warehouse)
    yield warehouse


def test_create_product(app_client: TestClient, insert_warehouse_mongo):
    warehouse_id = str(insert_warehouse_mongo["_id"])
    product_url = f'{settings.API_STR}cyc/warehouse/product/'

    product_data = {
        "products": [
            {
                "name": "Queso",
                "exp_date": "2026-03-16",
                "quantity": 23,
                "warehouse_id": warehouse_id
            }
        ]
    }

    response = app_client.post(product_url, json=product_data)
    assert response.status_code == 201
    result = response.json()

    for field in product_data["products"][0]:
        assert str(result[0][field]) == str(product_data["products"][0][field])


def test_create_warehouse(app_client: TestClient):
    warehouse_url = f'{settings.API_STR}cyc/warehouse/'

    warehouse_data = {
        "name": "Almacén secundario",
        "products": [
            {
                "id": str(uuid4()),
                "name": "Leche entera",
                "quantity": 34,
                "exp_date": "2025-03-16"
            }
        ]
    }

    response = app_client.post(warehouse_url, json=warehouse_data)
    assert response.status_code == 201
    result = response.json()

    for field in warehouse_data:
        assert str(result[field]) == str(warehouse_data[field])
