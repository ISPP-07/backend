from pathlib import Path
import openpyxl
from uuid import uuid4
from datetime import date

import pytest_asyncio
from pymongo.database import Database
from fastapi.testclient import TestClient

from src.core.config import settings
from src.core.utils.helpers import generate_alias

URL_PATIENT = f'{settings.API_STR}acat/patient'


@pytest_asyncio.fixture()
async def insert_patients_mongo(mongo_db: Database):
    mongo_db["Patient"].delete_many({})
    result = []
    patients = [
        {
            "_id": uuid4(),
            "name": "Paciente 1",
            "first_surname": "AAA",
            "second_surname": "BBB",
            "birth_date": "2023-02-28",
            "address": "Calle 1",
            "contact_phone": "123123123",
            "alias": generate_alias("Paciente 1", "AAA", "BBB"),
            "nid": "12343456M",
            "birth_date": "2023-02-28",
            "gender": "Man",
            "address": "Calle 1",
            "contact_phone": "123123123",
            "dossier_number": "1",
            "first_technician": "string",
            "registration_date": date.today().isoformat(),
            "observation": "string"
        },
        {
            "_id": uuid4(),
            "name": "Paciente 2",
            "first_surname": "AAA",
            "second_surname": "BBB",
            "birth_date": "2023-02-28",
            "address": "Calle 1",
            "contact_phone": "123123123",
            "alias": generate_alias('Paciente 2', 'AAA', 'BBB'),
            "nid": "12343456M",
            "birth_date": "2023-02-28",
            "gender": "Man",
            "address": "Calle 1",
            "contact_phone": "123123123",
            "dossier_number": "2",
            "first_technician": "string",
            "registration_date": date.today().isoformat(),
            "observation": "string"
        },
    ]
    for patient in patients:
        mongo_db['Patient'].insert_one(patient)
        result.append(patient)
    yield result


@pytest_asyncio.fixture()
async def insert_patient_to_delete(mongo_db: Database):
    patient = {
        "_id": uuid4(),
        "name": "Martin",
        "first_surname": "Romero",
        "second_surname": "Castillo",
        "alias": generate_alias('Martin', 'Romero', 'Castillo'),
        "nid": "16343456J",
        "birth_date": "2015-02-28",
        "gender": "Man",
        "address": "Calle Castilleja",
        "contact_phone": "123123123",
        "dossier_number": "12341324",
        "first_technician": None,
        "registration_date": date.today().isoformat(),
        "observation": None
    }
    mongo_db['Patient'].insert_one(patient)
    yield patient


def test_get_patient_details(
        app_client: TestClient,
        insert_patients_mongo,
        app_superuser):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    patient_id = str(insert_patients_mongo[0]["_id"])
    url = f'{URL_PATIENT}/{patient_id}'
    response = app_client.get(url, headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["dossier_number"] == str(
        insert_patients_mongo[0]["dossier_number"])
    assert response_data["name"] == str(insert_patients_mongo[0]["name"])
    assert response_data["first_surname"] == str(
        insert_patients_mongo[0]["first_surname"])


def test_create_patient(app_client: TestClient, app_superuser):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    patient_data = {
        "dossier_number": "1",
        "name": "Paciente 1",
        "first_surname": "AAA",
        "second_surname": "BBB",
        "birth_date": "2023-02-28",
        "address": "Calle 1",
        "contact_phone": "123123123",
        "nid": "62890716E",
        "first_technician": "string",
        "gender": "Man",
        "observation": "string"
    }

    response = app_client.post(
        url=URL_PATIENT, json=patient_data, headers=headers)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["registration_date"] == date.today(
    ).isoformat()
    assert response_data["alias"] == generate_alias(
        patient_data["name"],
        patient_data["first_surname"],
        patient_data["second_surname"])


def test_get_patients(
        app_client: TestClient,
        insert_patients_mongo,
        app_superuser):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    response = app_client.get(url=URL_PATIENT, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert 'elements' in result and 'total_elements' in result
    assert isinstance(result['elements'], list)
    for item, patient in zip(result['elements'], insert_patients_mongo):
        assert item["id"] == str(patient["_id"])
        assert item["name"] == patient["name"]
        assert item["address"] == patient["address"]
        assert item["alias"] == patient["alias"]
        assert item["nid"] == patient["nid"]


def test_upload_excel_patients(
        app_client: TestClient,
        mongo_db: Database,
        app_superuser):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    # Ruta del endpoint
    url = f'{settings.API_STR}acat/patient/excel'

    # Cargar el archivo Excel de prueba
    excel_file_path = Path(__file__).resolve(
    ).parent.parent / 'excel_test' / 'Pacientes.xlsx'

    # Enviar el archivo Excel al endpoint
    with open(excel_file_path, 'rb') as file:
        files = {
            "patients": (
                "Pacientes.xlsx",
                file,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        response = app_client.post(url=url, files=files, headers=headers)

    # Verificar que la respuesta sea exitosa
    assert response.status_code == 204

    # Cargar el archivo Excel en meoria
    wb = openpyxl.load_workbook(excel_file_path)
    ws = wb.active

    # Obtener los datos de los pacientes de la base de datos
    patients_db = list(mongo_db["Patient"].find())

    assert ws.cell(row=2, column=4).value in [p['nid'] for p in patients_db]


def test_update_patient(
        app_client: TestClient,
        insert_patients_mongo: list,
        app_superuser):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    patient = insert_patients_mongo[0]
    url = f"{URL_PATIENT}/{patient['_id']}"
    updated_fields = ['name', 'gender', 'second_surname', 'birth_date']
    not_updated_fields = [
        'dossier_number', 'first_surname', 'address', 'contact_phone',
        'alias', 'nid', 'first_technician', 'observation', 'registration_date'
    ]
    update_data = {
        'name': 'Antonio',
        'gender': None,
        'second_surname': None,
        'birth_date': "2001-09-20",
        'update_fields_to_none': ['gender', 'second_surname']
    }
    response = app_client.patch(url=url, json=update_data, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, dict)
    assert result['id'] == str(patient['_id'])
    for field in updated_fields:
        assert result[field] == update_data[field]
    for field in not_updated_fields:
        assert result[field] == patient[field]


def test_delete_patient(
    app_client: TestClient,
    insert_patient_to_delete,
    mongo_db: Database,
    app_superuser
):
    access_token = app_superuser['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    url = f"{URL_PATIENT}/{insert_patient_to_delete['_id']}"
    response = app_client.delete(url=url, headers=headers)
    assert response.status_code == 204
    deleted_patient = mongo_db["Patient"].find_one(
        {'_id': insert_patient_to_delete['_id']}
    )
    assert deleted_patient is None
