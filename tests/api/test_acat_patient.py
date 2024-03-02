import pytest_asyncio
from fastapi.testclient import TestClient

from src.core.config import settings

from src.modules.acat.patient.model import Patient


@pytest_asyncio.fixture
async def create_patients(session) -> list[Patient]:
    result = []
    patients_data = [
        {
            "registration_date": "2023-02-29",
            "dossier_number": "1",
            "name": "Paciente 1",
            "alias": "P1",
            "first_surname": "AAA",
            "second_surname": "BBB",
            "birth_date": "2023-02-29",
            "sex": "Male",
            "address": "Calle 1",
            "dni": "12343456M",
            "contact_phone": "123123123",
            "age": 1,
            "first_appointment_date": "2023-02-29"
        },
        {
            "registration_date": "2024-02-29",
            "dossier_number": "2",
            "name": "Paciente 2",
            "alias": "P2",
            "first_surname": "CCC",
            "second_surname": "DDD",
            "birth_date": "2024-02-29",
            "sex": "Male",
            "address": "Calle 2",
            "dni": "54343421M",
            "contact_phone": "321321321",
            "age": 0,
            "first_appointment_date": "2024-02-29"
        },
    ]
    for patient_data in patients_data:
        patient = await Patient.create(session, **patient_data)
        result.append(patient)
    return result


def test_get_patients(client: TestClient, create_patients: list[Patient]):
    url = f'{settings.API_STR}cyc/patient/list'
    response = client.get(url)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) == 2
    assert result == [patient.model_dump() for patient in create_patients]