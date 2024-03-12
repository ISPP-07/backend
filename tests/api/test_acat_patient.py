from uuid import uuid4
from fastapi.testclient import TestClient
import pytest_asyncio
from pymongo.database import Database
import datetime

from src.core.config import settings
from src.core.utils.helpers import generate_alias


@pytest_asyncio.fixture
async def insert_patients_mongo(mongo_db: Database):
    result = []
    patients = [
        {
            "_id": uuid4(),
            "dossier_number": "1",
            "name": "Paciente 1",
            "first_surname": "AAA",
            "second_surname": "BBB",
            "birth_date": "2023-02-28",
            "sex": "Male",
            "address": "Calle 1",
            "dni": "12343456M",
            "contact_phone": "123123123",
            "age": 1,
            "first_appointment_date": "2023-02-28"
        },
        {
            "_id": uuid4(),
            "dossier_number": "2",
            "name": "Paciente 2",
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
    for patient in patients:
        mongo_db['Patient'].insert_one(patient)
        result.append(patient)
    return result


def test_create_patient(app_client: TestClient):
    url = f'{settings.API_STR}acat/patient/'

    patient_data = {
        "name": "string",
        "first_surname": "string",
        "second_surname": "string",
        "nid": "string",
        "birth_date": "2012-02-26",
        "gender": "Man",
        "address": "string",
        "contact_phone": "string",
        "dossier_number": "string",
        "first_technician": "string",
        "observations": "string"
    }

    response = app_client.post(url=url, json=patient_data)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["registration_date"] == datetime.date.today(
    ).isoformat()
    assert response_data["alias"] == generate_alias(
        patient_data["name"],
        patient_data["first_surname"],
        patient_data["second_surname"])


# @pytest.mark.asyncio
# def test_get_patients(client: TestClient, create_patients: list[Patient]):
#     url = f'{settings.API_STR}acat/patient'
#     response = client.get(url)
#     assert response.status_code == 200
#     result = response.json()
#     assert isinstance(result, list)
#     assert len(result) == 2
#     assert result == [patient.model_dump() for patient in create_patients]


# @pytest.mark.asyncio
# async def test_get_patient_details(client: TestClient, create_patients:
# list[Patient]):

#     patient = create_patients.pop()

#     url_get = f'{settings.API_STR}acat/patient/details/{patient.id}'

#     response = client.get(url_get)

#     assert response.status_code == 200

#     response_data = response.json()
#     assert response_data["name"] == patient.name
#     assert response_data["alias"] == patient.alias
