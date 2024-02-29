import pytest
from src.modules.acat.appointment.model import Appointment
from fastapi.testclient import TestClient
from src.core.config import settings

@pytest.mark.asyncio
async def test_list_appointment(client: TestClient):
    url = f'{settings.API_STR}acat/appointment/'

    response = client.get(url)

    assert response.status_code == 200
    response_data = response.json()

    assert response_data[0]["appointment_date"] == "2023-01-01"
    assert response_data[0]["technician_id"] == 1
    assert len(response_data) == 3
    