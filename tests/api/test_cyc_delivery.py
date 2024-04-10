from uuid import uuid4

from fastapi.testclient import TestClient
import pytest_asyncio
from pymongo.database import Database

from src.core.config import settings

URL_DELIVERY = f'{settings.API_STR}cyc/delivery'


@pytest_asyncio.fixture
async def insert_deliveries_mongo(mongo_db: Database):
    result = []

    family = {
        "_id": uuid4(),
        "name": "familia Pedro TEST",
        "phone": "66666666",
        "address": "San Marcos",
        "referred_organization": None,
        "next_renewal_date": "2025-03-08",
        "observation": None,
        "number_of_people": 1,
        "informed": False,
        "members": [
                {
                    "date_birth": "2003-03-08",
                    "type": "Adult",
                    "name": "Pepe",
                    "surname": "Cast",
                    "nationality": "Spain",
                    "nid": "07344702C",
                    "family_head": True,
                    "gender": "Man",
                    "functional_diversity": True,
                    "food_intolerances": [],
                    "homeless": False
                }
        ]
    }

    mongo_db['Family'].insert_one(family)

    warehouse = {
        "_id": uuid4(),
        "name": "Warehouse",
        "products": [
            {
                "id": uuid4(),
                "name": "Product 1",
                "quantity": 10,
                "exp_date": "3000-04-08",
            }
        ]
    }

    mongo_db['Warehouse'].insert_one(warehouse)

    deliveries = [
        {
            "_id": uuid4(),
            "date": "2025-03-08",
            "months": 1,
            "state": "next",
            "lines": [
                {
                    "product_id": warehouse["products"][0]["id"],
                    "quantity": 1,
                    "state": "good",
                }
            ],
            "family_id": family["_id"],
        },
        {
            "_id": uuid4(),
            "date": "2025-03-08",
            "months": 2,
            "state": "next",
            "lines": [
                {
                    "product_id": warehouse["products"][0]["id"],
                    "quantity": 1,
                    "state": "good",
                }
            ],
            "family_id": family["_id"],
        },
    ]

    for delivery in deliveries:
        mongo_db['Delivery'].insert_one(delivery)
        result.append(delivery)
    yield result


def test_get_deliveries(app_client: TestClient, insert_deliveries_mongo, app_superuser):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    response = app_client.get(url=URL_DELIVERY, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert 'elements' in result and 'total_elements' in result
    assert isinstance(result['elements'], list)
    assert len(result['elements']) == 2
    for item, delivery in zip(result['elements'], insert_deliveries_mongo):
        assert item['id'] == str(delivery['_id'])
        # Convert the date string to ISO format without time
        item_date = item['date'].split('T')[0]
        assert item_date == delivery['date']
        assert item['months'] == delivery['months']
        assert item['lines'][0]['product_id'] == str(
            delivery['lines'][0]['product_id'])
        assert item['lines'][0]['quantity'] == delivery['lines'][0]['quantity']
        assert item['lines'][0]['state'] == delivery['lines'][0]['state']
        assert item['family_id'] == str(delivery['family_id'])


def test_get_delivery_detail(
    app_client: TestClient,
    insert_deliveries_mongo,
    app_superuser
):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    delivery_id = str(insert_deliveries_mongo[0]["_id"])
    url = f'{URL_DELIVERY}/{delivery_id}'
    response = app_client.get(url=url, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == delivery_id
    assert result["date"] == "2025-03-08T00:00:00"
    assert result["months"] == 1
    assert result["lines"][0]["product_id"] == str(
        insert_deliveries_mongo[0]["lines"][0]["product_id"])
    assert result["lines"][0]["quantity"] == insert_deliveries_mongo[0]["lines"][0]["quantity"]
    assert result["lines"][0]["state"] == insert_deliveries_mongo[0]["lines"][0]["state"]
    assert result["family_id"] == str(
        insert_deliveries_mongo[0]["family_id"])


def test_create_delivery(app_client: TestClient, insert_deliveries_mongo, app_superuser):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    data = {
        "date": "2025-03-08",
        "months": 1,
        "lines": [
            {
                "product_id": str(
                    insert_deliveries_mongo[0]["lines"][0]["product_id"]),
                "quantity": 1,
                "state": "good",
            }],
        "family_id": str(
            insert_deliveries_mongo[0]["family_id"]),
    }
    response = app_client.post(url=URL_DELIVERY, json=data, headers=headers)
    assert response.status_code == 201
    result = response.json()
    assert result["date"] == "2025-03-08T00:00:00"
    assert result["months"] == 1
    assert result["lines"][0]["product_id"] == data["lines"][0]["product_id"]
    assert result["lines"][0]["quantity"] == data["lines"][0]["quantity"]
    assert result["lines"][0]["state"] == data["lines"][0]["state"]
    assert result["family_id"] == data["family_id"]


def test_get_family_deliveries(
    app_client: TestClient,
    insert_deliveries_mongo: list,
    app_superuser
):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    family_id = str(insert_deliveries_mongo[0]['family_id'])
    url = f'{URL_DELIVERY}/family/{family_id}'
    response = app_client.get(url=url, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2


def test_update_delivery(
    app_client: TestClient,
    insert_deliveries_mongo: list,
    app_superuser
):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    delivery_id = str(insert_deliveries_mongo[0]["_id"])
    data = {
        "date": "3000-03-25",
        "lines": [
            {
                "product_id": str(
                    insert_deliveries_mongo[0]["lines"][0]["product_id"]),
                "quantity": 5,
                "state": "good",
            }],
        "family_id": str(
            insert_deliveries_mongo[0]["family_id"]),
    }
    url = f'{URL_DELIVERY}/{delivery_id}'
    response = app_client.patch(url=url, json=data, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == delivery_id
    assert result["date"] == "3000-03-25T00:00:00"
    assert result["lines"][0]["product_id"] == data["lines"][0]["product_id"]
    assert result["lines"][0]["quantity"] == data["lines"][0]["quantity"]
    assert result["lines"][0]["state"] == data["lines"][0]["state"]
    assert result["family_id"] == data["family_id"]


def test_delete_delivery(
    app_client: TestClient,
    insert_deliveries_mongo: list,
    app_superuser
):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    delivery_id = str(insert_deliveries_mongo[0]["_id"])
    url = f'{URL_DELIVERY}/{delivery_id}'
    response = app_client.delete(url=url, headers=headers)
    assert response.status_code == 204
