from datetime import datetime

from fastapi.testclient import TestClient
import pytest_asyncio

from src.core.config import settings


@pytest_asyncio.fixture
async def insert_families_mongo(app_client: TestClient):
    result = []
    families = [{
        "name": "familia Pedro TEST",
        "phone": "66666666",
        "address": "San Marcos",
        "number_of_people": 1,
        "referred_organization": None,
        "next_renewal_date": "2025-03-08",
        "observation": None,
        "members": [{
            "date_birth": "2003-03-08",
            "type": "Adult",
            "name": "Pepe",
            "surname": "Cast",
            "nationality": "Spain",
            "nid": "07344702C",
            "family_head": True,
            "gender": "Men",
            "functional_diversity": True,
            "food_intolerances": [],
            "homeless": False
        }]}]
    url_post_families = f'{settings.API_STR}cyc/family/'
    for family in families:
        response = app_client.post(url_post_families, json=family)
        result.append(response.json())
    yield result


def test_get_families(app_client: TestClient, insert_families_mongo):
    url = f'{settings.API_STR}cyc/family/'
    response = app_client.get(url=url)
    print('me ha dado respuest')
    assert response.status_code == 200
    result = response.json()
    print('----------------------------')
    for item in result:
        print(item)
    print('----------------------------')
    assert True
    assert isinstance(result, list)
    assert len(result) == 1
    for item, family in zip(result, insert_families_mongo):
        print('item', item)
        print('family', family)
        assert item['id'] == family['id']  # pylint: disable=W0212
        assert item['name'] == family['name']
        assert item['number_of_people'] == family['number_of_people']
        assert len(item['members']) == len(family['members'])
