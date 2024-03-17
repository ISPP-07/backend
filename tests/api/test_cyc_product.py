from uuid import uuid4
import pytest_asyncio
from fastapi.testclient import TestClient
from pymongo.database import Database

from src.core.config import settings


@pytest_asyncio.fixture
async def insert_warehouses_with_products(mongo_db: Database):
    # Clean the database
    mongo_db['Warehouse'].delete_many({})

    warehouse_id_1 = uuid4()
    warehouse_id_2 = uuid4()
    warehouses = [
        {"_id": warehouse_id_1,
            "name": "Almacén 1",
            "products": [
                {
                    "name": "Producto 1",
                    "quantity": 10,
                    "exp_date": "2025-01-01",
                    "warehouse_id": warehouse_id_1
                }
            ]
         },
        {"_id": warehouse_id_2,
            "name": "Almacén 2",
            "products": [
                {
                    "name": "Producto 2",
                    "quantity": 10,
                    "exp_date": "2025-01-01",
                    "warehouse_id": warehouse_id_2
                }
            ]
         }
    ]
    for warehouse in warehouses:
        mongo_db['Warehouse'].insert_one({**warehouse, "id": warehouse["_id"]})

    yield warehouses


def test_get_all_products_list(
        app_client: TestClient,
        insert_warehouses_with_products):
    warehouses = insert_warehouses_with_products
    url_get = f'{settings.API_STR}cyc/warehouse/product'
    response = app_client.get(url_get)
    assert response.status_code == 200
    response_data = response.json()

    inserted_products = [
        product for warehouse in warehouses for product in warehouse["products"]]

    assert len(response_data) == len(inserted_products)
    for product_data in response_data:
        assert any(product_data["name"] == product["name"] and product_data["quantity"]
                   == product["quantity"] for product in inserted_products)
