from pydantic import UUID4

from fastapi import HTTPException, status

from src.core.utils.helpers import calculate_age, generate_alias
from src.modules.acat.patient import service
from src.modules.acat.patient import model
from src.core.deps import DataBaseDep


async def get_patients_controller(db: DataBaseDep):
    return await service.get_patients_service(db)


async def create_patient_controller(db: DataBaseDep, patient: model.PatientCreate) -> model.Patient:
    mongo_insert = await service.create_patient_service(db, patient)
    result = await service.get_patient_service(db, query={'id': mongo_insert.inserted_id})
    return result


async def get_patient_details_controller(db: DataBaseDep, patient_id: UUID4):
    result = await service.get_patient_service(db, query={'id': patient_id})
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Patient not found',
        )
    return result


async def update_patient_controller(db: DataBaseDep,
            patient_id: UUID4,
            patient: model.PatientUpdate) -> model.Patient:
    existing_patient = await service.get_patient_service(db, query={'id': patient_id})
    if existing_patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Patient not found',
        )

    updated_patient_data = {
        'name': existing_patient.name
            if patient.name is None
            else patient.name,
        'first_surname': existing_patient.first_surname
            if patient.first_surname is None
            else patient.first_surname,
        'second_surname': existing_patient.second_surname
            if patient.second_surname is None
            else patient.second_surname,
        'nid': existing_patient.nid
            if patient.nid is None
            else patient.nid,
        'birth_date': existing_patient.birth_date
            if patient.birth_date is None
            else patient.birth_date,
        'gender': existing_patient.gender
            if patient.gender is None
            else patient.gender,
        'address': existing_patient.address
            if patient.address is None
            else patient.address,
        'contact_phone': existing_patient.contact_phone
            if patient.contact_phone is None
            else patient.contact_phone,
        'dossier_number': existing_patient.dossier_number
            if patient.dossier_number is None
            else patient.dossier_number,
        'first_technician': existing_patient.first_technician
            if patient.first_technician is None
            else patient.first_technician,
        'observations': existing_patient.observations
            if patient.observations is None
            else patient.observations,
    }

    updated_patient = await service.update_patient_service(db,patient_id, updated_patient_data)

    return updated_patient
