from uuid import uuid4
from fastapi.testclient import TestClient
import pytest_asyncio
from pymongo.database import Database
import datetime

from src.core.config import settings
from src.core.utils.helpers import generate_alias


@pytest_asyncio.fixture()
async def insert_patients_mongo(mongo_db: Database):
    mongo_db["Patient"].delete_many({})
    result = []
    patients = [
        {
            "_id": uuid4(),
            "dossier_number": "1",
            "name": "Paciente 1",
            "first_surname": "AAA",
            "second_surname": "BBB",
            "birth_date": "2023-02-28",
            "address": "Calle 1",
            "contact_phone": "123123123",
            "alias": "Paciente 1 AAA BBB",
            "nid": "12343456M",
            "first_technician": "string",
            "gender": "Man",
            "observations": "string"
        },
        {
            "_id": uuid4(),
            "dossier_number": "2",
            "name": "Paciente 2",
            "first_surname": "AAA",
            "second_surname": "BBB",
            "birth_date": "2023-02-28",
            "address": "Calle 1",
            "contact_phone": "123123123",
            "alias": "Paciente 1 AAA BBB",
            "nid": "12343456M",
            "first_technician": "string",
            "gender": "Man",
            "observations": "string"
        },
    ]
    for patient in patients:
        mongo_db['Patient'].insert_one(patient)
        result.append(patient)
    yield result


def test_get_patient_details(app_client: TestClient, insert_patients_mongo):
    patient_id = str(insert_patients_mongo[0]["_id"])

    url_get = f'{settings.API_STR}acat/patient/{patient_id}'
    response = app_client.get(url_get)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["dossier_number"] == str(
        insert_patients_mongo[0]["dossier_number"])
    assert response_data["name"] == str(insert_patients_mongo[0]["name"])
    assert response_data["first_surname"] == str(
        insert_patients_mongo[0]["first_surname"])


def test_create_patient(app_client: TestClient):
    url = f'{settings.API_STR}acat/patient/'

    patient_data = {
        "dossier_number": "1",
        "name": "Paciente 1",
        "first_surname": "AAA",
        "second_surname": "BBB",
        "birth_date": "2023-02-28",
        "address": "Calle 1",
        "contact_phone": "123123123",
        "alias": "Paciente 1 AAA BBB",
        "nid": "12343456M",
        "first_technician": "string",
        "gender": "Man",
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


def test_get_patients(
        app_client: TestClient,
        insert_patients_mongo,
        mongo_db: Database):
    url = f'{settings.API_STR}acat/patient'

    test = mongo_db["Patient"].find()
    for x in test:
        print(x)

    response = app_client.get(url=url)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    for item, patient in zip(result, insert_patients_mongo):
        assert item["id"] == str(patient["_id"])
        assert item["name"] == patient["name"]
        assert item["address"] == patient["address"]
        assert item["alias"] == patient["alias"]
        assert item["nid"] == patient["nid"]


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
