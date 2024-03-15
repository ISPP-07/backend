from datetime import datetime
from uuid import uuid4
from pymongo.database import Database
import pytest_asyncio
from fastapi.testclient import TestClient
from src.core.config import settings


# Fixture para insertar una familia de ejemplo en MongoDB


@pytest_asyncio.fixture
async def insert_family_mongo(mongo_db: Database):
    family = {
        "id": uuid4(),
        "name": "Los García",
        "phone": "987654321",
        "address": "Calle Falsa 123",
        "referred_organization": "Org Referida",
        "next_renewal_date": datetime(2025, 1, 1).isoformat(),
        "derecognition_state": "Active",
        "observation": "Ninguna observación",
        "number_of_people": 4,
        "informed": True,
        "members": [
            {
                "date_birth": "2010-05-01",
                "type": "Child",
                "name": "Luis",
                "surname": "García",
                "nationality": "Española",
                "nid": "12345678A",
                "family_head": False,
                "gender": "Man",
                "functional_diversity": False,
                "food_intolerances": [],
                "homeless": False
            }
            # Puedes agregar más miembros según sea necesario
        ]
    }

    mongo_db['Family'].insert_one(family)
    yield family


def test_create_family(app_client: TestClient, insert_family_mongo):
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
            # Puedes añadir más miembros según sea necesario
        ]
    }

    response = app_client.post(url=url, json=family_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == family_data["name"]
    assert response_data["address"] == family_data["address"]
