import pytest_asyncio
from fastapi.testclient import TestClient

from src.core.config import settings

from src.modules.cyc.family.model import Family, Person


@pytest_asyncio.fixture
async def create_family(session) -> Family:
    person1_data = {
        "date_birth": "2005-01-01",
        "type": "Child",
        "name": "Jane Doe",
        "dni": "87654321",
        "family_id": "1"
    }

    person2_data = {
        "date_birth": "2000-01-01",
        "type": "Adult",
        "name": "John Doe",
        "dni": "12345678",
        "family_id": "1"
    }

    await Person.create(session, **person1_data)
    await Person.create(session, **person2_data)

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
    }
    family = await Family.create(session, **family_data)

    return family


def test_get_family_details(client: TestClient, create_family: Family):
    family_id = create_family.id
    url = (f'{settings.API_STR}cyc/family/'  + str(family_id))

    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["id"] == family_id
