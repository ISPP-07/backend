from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from pymongo.database import Database

from src.core.config import settings


@pytest.fixture
def insert_families_mongo(mongo_db: Database):
    # Clean the database
    mongo_db['Family'].delete_many({})

    result = []
    families = [
        {
            "_id": uuid4(),
            "name": "familia Pedro TEST",
            "phone": "66666666",
            "address": "San Marcos",
            "referred_organization": None,
            "next_renewal_date": "2025-03-08",
            "observation": None,
            "number_of_people": 2,
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
                },
                {
                    "date_birth": "2023-03-08",
                    "type": "Child",
                    "name": "Jose",
                    "surname": "Cast",
                    "nationality": "Spain",
                    "nid": "37210711T",
                    "family_head": False,
                    "gender": "Man",
                    "functional_diversity": True,
                    "food_intolerances": [],
                    "homeless": False
                }
            ]
        }
    ]
    for family in families:
        mongo_db['Family'].insert_one(family)
        result.append(family)
    yield result


def test_get_families(app_client: TestClient, insert_families_mongo):
    url = f'{settings.API_STR}cyc/family/'
    response = app_client.get(url=url)
    assert response.status_code == 200
    result = response.json()
    assert True
    assert isinstance(result, list)
    assert len(result) == 1
    for item, family in zip(result, insert_families_mongo):
        assert item['id'] == str(family['_id'])
        assert item['name'] == family['name']
        assert item['number_of_people'] == family['number_of_people']
        assert len(item['members']) == len(family['members'])


def test_create_family(app_client: TestClient):
    url = f'{settings.API_STR}cyc/family/'
    family_data = {
        "name": "La Familia Pérez",
        "phone": "123456789",
        "address": "456 Main St",
        "referred_organization": "Hospital XYZ",
        "next_renewal_date": "2025-12-31",
        "observation": "Una observación",
        "members": [
            {
                "date_birth": "1985-08-25",
                "type": "Adult",
                "name": "Maria",
                "surname": "Pérez",
                "nationality": "Española",
                "nid": "51506994N",
                "family_head": True,
                "gender": "Woman",
                "functional_diversity": False,
                "food_intolerances": [],
                "homeless": False
            }
        ]
    }

    response = app_client.post(url=url, json=family_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == family_data["name"]
    assert response_data["address"] == family_data["address"]


def test_get_family_details(app_client: TestClient, insert_families_mongo):
    family = insert_families_mongo[0]
    family_id = family['_id']
    url = f'{settings.API_STR}cyc/family/{family_id}'

    response = app_client.get(url)
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == str(family_id)

    for field in family:
        if field == '_id':
            assert str(result['id']) == str(family[field])
        else:
            assert str(result[field]) == str(family[field])


def test_update_family(app_client: TestClient, insert_families_mongo):
    family = insert_families_mongo[0]
    family_id = family['_id']
    url = f'{settings.API_STR}cyc/family/{family_id}'

    # Solo actualizo algunos campos de la familia
    family_data = {
        "name": "La Familia Rodriguez",
        "address": "Calle Principal 456",
        "referred_organization": "Hospital ABC"
    }

    response = app_client.patch(url=url, json=family_data)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == family_data["name"]
    assert response_data["address"] == family_data["address"]
    assert response_data["referred_organization"] == family_data["referred_organization"]


def test_delete_family(app_client: TestClient, insert_families_mongo):
    family = insert_families_mongo[0]
    family_id = family['_id']
    url = f'{settings.API_STR}cyc/family/{family_id}'

    response = app_client.delete(url)
    assert response.status_code == 204

    response = app_client.get(url)
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "Family not found"
