import pytest_asyncio
from fastapi.testclient import TestClient

from src.core.config import settings

from src.modules.cyc.family.model import Family, FamilyObservation, Person


@pytest_asyncio.fixture
async def create_family(session) -> Family:
    family_data = {
        "id": 1,
        "name": "La Familia",
        "phone": "123456789",
        "address": "123 Main St",
        "number_of_people": 4,
        "referred_organization": "Hospital ABC",
        "next_renewal_date": "2100-12-31",
        "derecognition_state": "Active",
    }

    family = await Family.create(session, **family_data)

    observations_data = [
        {"observation_text": "Observation 1", "family_id": family.id},
        {"observation_text": "Observation 2", "family_id": family.id},
    ]

    for obs_data in observations_data:
        await FamilyObservation.create(session, **obs_data)

    person1_data = {
        "date_birth": "2005-01-01",
        "type": "Child",
        "name": "Jane Doe",
        "dni": "87654321",
        "family_id": family.id
    }

    person2_data = {
        "date_birth": "2000-01-01",
        "type": "Adult",
        "name": "John Doe",
        "dni": "12345678",
        "family_id": family.id
    }

    await Person.create(session, **person1_data)
    await Person.create(session, **person2_data)

    return family


def test_get_family_details(client: TestClient, create_family: Family):
    family_id = create_family.id
    url = f'{settings.API_STR}cyc/family/' + str(family_id)

    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["id"] == family_id
