import pytest
from fastapi.testclient import TestClient

from src.core.config import settings

from src.modules.cyc.family.model import Family


@pytest.mark.asyncio
async def create_family_test(client: TestClient) -> Family:
    create_family_url = f'{settings.API_STR}acat/family/'

    person1_data = {
        "date_birth": "2005-01-01",
        "type": "Child",
        "name": "Jane Doe",
        "dni": "87654321"
    }

    person2_data = {
        "date_birth": "2000-01-01",
        "type": "Adult",
        "name": "John Doe",
        "dni": "12345678"
    }
    family_data = {
        "id": 1,
        "name": "La Familia",
        "phone": "123456789",
        "address": "123 Main St",
        "number_of_people": 4,
        "referred_organization": "Hospital ABC",
        "next_renewal_date": "2100-12-31",
        "derecognition_state": "Active",
        "obsarvations": "Observation 1",
        "members": [
            person1_data,
            person2_data
        ]
    }
    response = client.post(create_family_url, json=family_data)
    assert response.status_code == 201
    response_data = response.json()
    return response_data


@pytest.mark.asyncio
async def test_get_family_details(client: TestClient):
    family = await create_family_test(client)
    family_id = family["id"]
    url = (f'{settings.API_STR}'
           f'cyc/family/details/' + str(family_id))

    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == family
