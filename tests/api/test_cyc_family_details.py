from uuid import uuid4

import pytest_asyncio
from fastapi.testclient import TestClient
from pymongo.database import Database

from src.core.config import settings


@pytest_asyncio.fixture
async def insert_family_mongo(mongo_db: Database):
    family_data = {
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

    mongo_db['Family'].insert_one(family_data)

    return family_data


def test_get_family_details(app_client: TestClient, insert_family_mongo):
    family = insert_family_mongo
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
