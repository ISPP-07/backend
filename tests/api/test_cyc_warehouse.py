from pathlib import Path
from uuid import uuid4
import openpyxl
import pytest_asyncio
from fastapi.testclient import TestClient
from pymongo.database import Database
from httpx import Response

from src.core.config import settings


@pytest_asyncio.fixture
async def insert_warehouses_with_products(mongo_db: Database):
    mongo_db['Warehouse'].delete_many({})

    warehouse_id_1 = uuid4()
    warehouse_id_2 = uuid4()
    warehouse_id_3 = uuid4()
    warehouses = [
        {"_id": warehouse_id_1,
            "name": "Almacén 1",
            "products": [
                {
                    "id": uuid4(),
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
                    "id": uuid4(),
                    "name": "Producto 2",
                    "quantity": 10,
                    "exp_date": "2025-01-01",
                    "warehouse_id": warehouse_id_2
                }
            ]
         },
        {"_id": warehouse_id_3,
            "name": "Sevilla Este",
            "products": []
         }
    ]
    for warehouse in warehouses:
        mongo_db['Warehouse'].insert_one(warehouse)

    yield warehouses


def test_get_all_products_list(
    app_client: TestClient,
    insert_warehouses_with_products
):
    warehouses = insert_warehouses_with_products
    url_get = f'{settings.API_STR}cyc/warehouse/product'
    response: Response = app_client.get(url_get)
    print(response.text)
    assert response.status_code == 200
    response_data = response.json()

    inserted_products = [
        product for warehouse in warehouses for product in warehouse["products"]]

    assert len(response_data) == len(inserted_products)
    for product_data in response_data:
        assert any(product_data["name"] == product["name"] and product_data["quantity"]
                   == product["quantity"] for product in inserted_products)


def test_create_product(
        app_client: TestClient,
        insert_warehouses_with_products):
    warehouse_id = str(insert_warehouses_with_products[0]["_id"])
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


def test_upload_excel_products(app_client: TestClient, mongo_db: Database):
    # Ruta del endpoint
    url = f'{settings.API_STR}cyc/warehouse/product/excel'

    # Cargar el archivo Excel de prueba
    excel_file_path = Path(__file__).resolve(
    ).parent.parent / 'excel_test' / 'Almacenes.xlsx'

    # Enviar el archivo Excel al endpoint
    with open(excel_file_path, 'rb') as file:
        files = {"products": (
            "Almacenes.xlsx", file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        response = app_client.post(url=url, files=files)

    # Verificar que la respuesta sea exitosa
    assert response.status_code == 204

    # Cargar el archivo Excel en meoria
    wb = openpyxl.load_workbook(excel_file_path)
    ws = wb.active

    # Obtener los datos de los productos de la base de datos
    warehouse_db = mongo_db["Warehouse"].find_one(
        {"name": ws.cell(row=2, column=4).value})
    products_db = list(warehouse_db["products"])

    # Obtener el primer producto creado
    first_product = products_db[0]

    # Comparar los datos del primer producto creado con los del archivo Excel
    assert first_product['name'] == ws.cell(row=2, column=1).value
    assert first_product['quantity'] == ws.cell(row=2, column=2).value
    assert first_product['exp_date'] == ws.cell(row=2, column=3).value
