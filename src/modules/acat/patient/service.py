from fastapi import HTTPException, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.modules.acat.patient import model
from src.core.database.mongo_types import InsertOneResultMongo, UpdateResult


async def get_patient_by_id(db: DataBaseDep, patient_id: UUID4):
    return await model.Patient.get(db, query={'id': patient_id})


async def get_patients_service(db: DataBaseDep, query=None) -> list[model.Patient]:
    return await model.Patient.get_multi(db, query)


async def create_patient_service(db: DataBaseDep, patient: model.PatientCreate) -> InsertOneResultMongo:
    result: InsertOneResultMongo = await model.Patient.create(db, obj_to_create=patient.model_dump())
    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    return result


async def update_one_patient_service(
    db: DataBaseDep,
    query: dict,
    update: model.PatientUpdate,
    **kwargs
) -> UpdateResult:
    return await model.Patient.update(
        db=db,
        query=query,
        data_to_update=update.model_dump(),
        **kwargs
    )


async def update_many_patient_service(
    db: DataBaseDep,
    query: dict,
    update: model.PatientUpdate,
    **kwargs
) -> UpdateResult:
    return await model.Patient.update_many(
        db=db,
        query=query,
        data_to_update=update,
        **kwargs
    )


async def get_patient_service(db: DataBaseDep, query: dict) -> model.PatientOut | None:
    patient: model.Patient = await model.Patient.get(db, query)

    if not patient:
        return None

    # Add age to the patient
    patient_dict = patient.model_dump()
    patient_dict['age'] = patient.age()

    return model.PatientOut(**patient_dict)
