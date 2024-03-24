from fastapi import HTTPException, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.modules.acat.patient import model
from src.modules.acat.patient import service


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


async def update_patient_controller(
    db: DataBaseDep,
    patient_id: UUID4,
    patient: model.PatientUpdate
) -> model.Patient:
    patient_db = await service.get_patient_service(db, query={'id': patient_id})
    if patient_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Patient not found',
        )
    if patient.nid is not None:
        check_nid = await service.get_patient_service(db, query={'nid': patient.nid})
        if check_nid is not None and check_nid.id != patient_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'There is already a patient with nid {patient.nid}',
            )
    none_fields = [
        'second_surname', 'gender', 'address',
        'contact_phone', 'first_technician', 'observation'
    ]
    request_none_fields = [
        field for field in none_fields
        if field in patient.update_fields_to_none
    ]
    update_data = patient.model_dump()
    for field in update_data.copy():
        if field in request_none_fields:
            continue
        if update_data[field] is None:
            update_data.pop(field)
    updated_patient = await service.update_patient_service(db, patient_id, update_data)
    return updated_patient


async def delete_patient_controller(db: DataBaseDep, patient_id: UUID4):
    await service.delete_patient_service(db, query={'id': patient_id})
