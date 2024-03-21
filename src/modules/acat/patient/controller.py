from pydantic import UUID4

from fastapi import HTTPException, status

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
