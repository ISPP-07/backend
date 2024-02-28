import pytest
from src.modules.acat.patient.model import Patient
from fastapi.testclient import TestClient
from src.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_create_patient(client: TestClient):
    url = f'{settings.API_STR}acat/patient/'

    patient_data = {
        "id": 0,
        "registration_date": "2024-02-26",
        "dossier_number": "string",
        "name": "string",
        "alias": "string",
        "first_surname": "string",
        "second_surname": "string",
        "birth_date": "2024-02-26",
        "sex": "Male",
        "address": "string",
        "dni": "string",
        "contact_phone": "string",
        "age": 0,
        "first_appointment_date": "2024-02-26"
    }

    response = client.post(url, json=patient_data)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == patient_data["name"]
    assert response_data["alias"] == patient_data["alias"]

@pytest.mark.asyncio
async def test_get_patient_details(client: TestClient): 

    patient_data = {
        "id": 1,
        "registration_date": "2024-02-26",
        "dossier_number": "string",
        "name": "string",
        "alias": "string",
        "first_surname": "string",
        "second_surname": "string",
        "birth_date": "2024-02-26",
        "sex": "Male",
        "address": "string",
        "dni": "string",
        "contact_phone": "string",
        "age": 0,
        "first_appointment_date": "2024-02-26"
    }

    url_get = f'{settings.API_STR}acat/patient/details/{patient_data["id"]}'
    url_post = f'{settings.API_STR}acat/patient'
    
    client.post(url_post, json=patient_data)
    response = client.get(url_get)
    
    assert response.status_code == 200
    
    response_data = response.json()
    assert response_data["name"] == patient_data["name"]
    assert response_data["alias"] == patient_data["alias"]
    
