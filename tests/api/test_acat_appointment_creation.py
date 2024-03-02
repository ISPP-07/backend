import pytest
from fastapi.testclient import TestClient
from src.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.acat.patient.model import Patient, Technician
from src.modules.shared.user.model import User


@pytest.mark.asyncio
async def test_create_appointment(client: TestClient, session: AsyncSession):
    url = f'{settings.API_STR}acat/appointment/'

    patient_data = {
            "registration_date": "2024-02-29",
            "dossier_number": "123456",
            "name": "John",
            "alias": "Johnny",
            "first_surname": "Doe",
            "second_surname": "Smith",
            "birth_date": "1990-05-20",
            "sex": "MALE",
            "address": "123 Main St",
            "dni": "12345678A",
            "contact_phone": "555-1234",
            "age": 32,
            "first_appointment_date": "2024-02-29"
        }
    
    technician_data = {
        "name": "John Doe",
        "user_id": 1
    }

    user_data = {
        "username": "john_doe",
        "password": "password",
        "email": "hola@hola.com"
    }


    await User.create(session, **user_data)
    await Patient.create(session, **patient_data)
    await Technician.create(session, **technician_data)

    appointment_data = {
            "id": 0,
            "technician_id": 1,
            "appointment_date": "2024-02-29",
            "patient_id": 1
        }

    response = client.post(url, json=appointment_data)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["appointment_date"] == appointment_data["appointment_date"]
    assert response_data["patient_id"] == appointment_data["patient_id"]
    assert response_data["technician_id"] == appointment_data["technician_id"]
        