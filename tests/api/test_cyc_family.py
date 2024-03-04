import pytest_asyncio
from fastapi.testclient import TestClient

from src.core.config import settings

from src.modules.cyc.family.model import Family


@pytest_asyncio.fixture
async def create_families(session) -> list[Family]:
    result = []
    families_data = [
        {
            "name": "La Familia",
            "phone": "123456789",
            "address": "123 Main St",
            "number_of_people": 4,
            "referred_organization": "Hospital ABC",
            "next_renewal_date": "2100-12-31",
            "derecognition_state": "Active"
        },
        {
            "name": "La Familia 2",
            "phone": "433456889",
            "address": "123 Main St 1º",
            "number_of_people": 8,
            "referred_organization": "Comedor ABC",
            "next_renewal_date": "2100-08-20",
            "derecognition_state": "Active"
        },
    ]
    for family_data in families_data:
        family = await Family.create(session, **family_data)
        result.append(family)
    return result


def test_get_families(client: TestClient, create_families: list[Family]):
    url = f'{settings.API_STR}cyc/family/'
    response = client.get(url)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) == 2
    assert result == [family.model_dump() for family in create_families]
