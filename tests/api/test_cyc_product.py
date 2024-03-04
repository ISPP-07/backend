from fastapi.testclient import TestClient
import pytest_asyncio
from src.core.config import settings

from src.modules.cyc.product.model import Product, Warehouse


@pytest_asyncio.fixture
async def create_products(session) -> list[Product]:
    result = []
    products_data = [{
        "id": 1,
        "name": "string",
        "quantity": 1,
        "exp_date": "2024-03-02",
        "warehouse_id": 1
    }, {
        "id": 2,
        "name": "string",
        "quantity": 1,
        "exp_date": "2024-03-02",
        "warehouse_id": 1
    }]
    warehouse_data = {
        "id": 1,
        "name": "string"
    }
    await Warehouse.create(session, **warehouse_data)
    for product_data in products_data:
        product = await Product.create(session, **product_data)
        result.append(product)
    return result


def test_get_products(client: TestClient, create_products: list[Product]):
    url = f'{settings.API_STR}cyc/product'
    response = client.get(url)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) == 2
    assert result == [patient.model_dump() for patient in create_products]
