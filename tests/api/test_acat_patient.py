# import pytest
# from fastapi.testclient import TestClient
# import pytest_asyncio

# from src.core.config import settings
# from src.modules.acat.patient.model import Patient


# @pytest_asyncio.fixture
# async def create_patients(session) -> list[Patient]:
#     result = []
#     patients_data = [
#         {
#             "registration_date": "2023-02-28",
#             "dossier_number": "1",
#             "name": "Paciente 1",
#             "alias": "P1",
#             "first_surname": "AAA",
#             "second_surname": "BBB",
#             "birth_date": "2023-02-28",
#             "sex": "Male",
#             "address": "Calle 1",
#             "dni": "12343456M",
#             "contact_phone": "123123123",
#             "age": 1,
#             "first_appointment_date": "2023-02-28"
#         },
#         {
#             "registration_date": "2024-02-29",
#             "dossier_number": "2",
#             "name": "Paciente 2",
#             "alias": "P2",
#             "first_surname": "CCC",
#             "second_surname": "DDD",
#             "birth_date": "2024-02-29",
#             "sex": "Male",
#             "address": "Calle 2",
#             "dni": "54343421M",
#             "contact_phone": "321321321",
#             "age": 0,
#             "first_appointment_date": "2024-02-29"
#         },
#     ]
#     for patient_data in patients_data:
#         patient = await Patient.create(session, **patient_data)
#         result.append(patient)
#     return result


# @pytest.mark.asyncio
# async def test_create_patient(client: TestClient):
#     url = f'{settings.API_STR}acat/patient/'

#     patient_data = {
#         "id": 0,
#         "registration_date": "2024-02-26",
#         "dossier_number": "string",
#         "name": "string",
#         "alias": "string",
#         "first_surname": "string",
#         "second_surname": "string",
#         "birth_date": "2024-02-26",
#         "sex": "Male",
#         "address": "string",
#         "dni": "string",
#         "contact_phone": "string",
#         "age": 0,
#         "first_appointment_date": "2024-02-26"
#     }

#     response = client.post(url, json=patient_data)

#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["name"] == patient_data["name"]
#     assert response_data["alias"] == patient_data["alias"]


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
