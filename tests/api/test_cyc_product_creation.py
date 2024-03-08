# import pytest
# from fastapi.testclient import TestClient
# from src.core.config import settings


# @pytest.mark.asyncio
# async def test_create_warehouse_and_product(client: TestClient):
#     warehouse_url = f'{settings.API_STR}cyc/product/warehouse/'
#     product_url = f'{settings.API_STR}cyc/product/'

#     # Create a warehouse
#     warehouse_data = {
#         "name": "Warehouse 1",
#     }
#     warehouse_response = client.post(warehouse_url, json=warehouse_data)
#     assert warehouse_response.status_code == 201
#     assert warehouse_response.json()["name"] == warehouse_data["name"]
#     assert warehouse_response.json()["id"] is not None

#     warehouse_id = warehouse_response.json()["id"]

#     # Create a product with the warehouse_id
#     product_data = {
#         "name": "Product 1",
#         "quantity": 10,
#         "exp_date": "2100-12-31",
#         "warehouse_id": warehouse_id
#     }

#     product_response = client.post(product_url, json=product_data)

#     assert product_response.status_code == 201
#     response_data = product_response.json()
#     assert response_data["name"] == product_data["name"]
#     assert response_data["quantity"] == product_data["quantity"]
#     assert response_data["exp_date"] == product_data["exp_date"]
#     assert response_data["warehouse_id"] == product_data["warehouse_id"]
#     assert response_data["id"] is not None
