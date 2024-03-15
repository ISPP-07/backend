from uuid import uuid4
import datetime

from fastapi.testclient import TestClient
import pytest_asyncio
from pymongo.database import Database
from src.core.utils.helpers import generate_alias
from tests.api.test_acat_patient import insert_patients_mongo

from src.core.config import settings


@pytest_asyncio.fixture
async def insert_interventions_mongo(mongo_db: Database):
    result = []
    patient = {
        "id": uuid4(),
        "name": "Pepe",
        "first_surname": "Cast",
        "second_surname": "Cast2",
        "nid": "07344702C",
        "birth_date": "2003-03-08",
        "gender": "Man",
        "address": "Calle 1",
        "contact_phone": "666666666",
        "dossier_number": "1",
        "first_technician": "John Doe",
        "observations": "Observations"
    }

    patient["alias"] = generate_alias(
        patient["name"],
        patient["first_surname"],
        patient["second_surname"])
    patient["registration_date"] = datetime.date.today().isoformat()

    mongo_db['Patient'].insert_one(patient)

    interventions = [
        {
            "_id": uuid4(),
            "date": "2025-03-08",
            "reason": "Food intervention",
            "typology": "Food",
            "observations": "Food intervention",
            "technician": "John Doe",
            "patient": patient,
        },
        {
            "_id": uuid4(),
            "date": "2025-03-08",
            "reason": "Food intervention2",
            "typology": "Food2",
            "observations": "Food intervention2",
            "technician": "John Doe",
            "patient": patient,
        },
    ]

    for intervention in interventions:
        mongo_db['Intervention'].insert_one(intervention)
        result.append(intervention)
    yield result


def test_get_intervention_detail(
        app_client: TestClient,
        insert_interventions_mongo):
    intervention_id = str(insert_interventions_mongo[0]["_id"])
    url = f'{settings.API_STR}acat/intervention/{intervention_id}'
    response = app_client.get(url=url)
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == intervention_id
    assert result["reason"] == "Food intervention"
    assert result["typology"] == "Food"
    assert result["observations"] == "Food intervention"
    assert result["technician"] == "John Doe"
    assert result["patient"]["id"] == str(
        insert_interventions_mongo[0]["patient"]["id"])
    assert result["patient"]["name"] == "Pepe"
    assert result["patient"]["first_surname"] == "Cast"
    assert result["patient"]["second_surname"] == "Cast2"
    assert result["patient"]["alias"] == "pecaca"
    assert result["patient"]["nid"] == "07344702C"
    assert result["patient"]["birth_date"] == "2003-03-08"


def test_create_intervention(app_client: TestClient, insert_patients_mongo):
    patient_id = str(insert_patients_mongo[0]["_id"])
    url = f'{settings.API_STR}acat/intervention/'
    intervention_data = {
        "date": "2023-03-03",
        "reason": "Food intervention",
        "typology": "Food",
        "observations": "Food intervention",
        "patient_id": patient_id,
        "technician": "John Doe"
    }
    response = app_client.post(url=url, json=intervention_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["date"] == intervention_data["date"]
    assert response_data["reason"] == intervention_data["reason"]
    assert response_data["typology"] == intervention_data["typology"]
    assert response_data["observations"] == intervention_data["observations"]
    assert response_data["technician"] == intervention_data["technician"]