from uuid import uuid4

from fastapi.testclient import TestClient
import pytest
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
