import pytest
from src.modules.acat.patient.model import Patient
from fastapi.testclient import TestClient
from src.core.config import settings


@pytest.mark.asyncio
async def test_create_family(client: TestClient):
    url = f'{settings.API_STR}cyc/family/'

    family_data = {
        "id": 1,
        "name": "La Familia",
        "phone": "123456789",
        "address": "123 Main St",
        "number_of_people": 4,
        "referred_organization": "Hospital ABC",
        "next_renewal_date": "2024-02-26",
        "derecognition_state": "Active"
    }

    response = client.post(url, json=family_data)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == family_data["name"]
    assert response_data["address"] == family_data["address"]
