
from pydantic import UUID4
from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.modules.acat.patient import model
from src.core.database.mongo_types import InsertOneResultMongo, DeleteResultMongo
from src.core.utils.helpers import generate_alias


async def get_patient_by_id(db: DataBaseDep, query):
    return await model.Patient.get(db, query=query)


async def get_patients_service(db: DataBaseDep) -> list[model.Patient]:
    return await model.Patient.get_multi(db)


async def create_patient_service(db: DataBaseDep,
            patient: model.PatientCreate) -> InsertOneResultMongo:
    # Add alias to the patient
    patient_dict = patient.model_dump()
    patient_dict['alias'] = generate_alias(
        patient_dict['name'],
        patient_dict['first_surname'],
        patient_dict['second_surname']
    )

    result: InsertOneResultMongo = await model.Patient.create(db, obj_to_create=patient_dict)
    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    return result


async def get_patient_service(db: DataBaseDep, query: dict) -> model.PatientOut | None:
    patient: model.Patient = await model.Patient.get(db, query)

    if not patient:
        return None

    # Add age to the patient
    patient_dict = patient.model_dump()
    patient_dict['age'] = patient.age()

    return model.PatientOut(**patient_dict)


async def update_patient_service(db: DataBaseDep, patient_id: UUID4,
                                 updated_patient_data: dict) -> model.Patient | None:
    return await model.Patient.update(
        db,
        query={'id': patient_id},
        data_to_update=updated_patient_data
    )

async def delete_patient_service(db: DataBaseDep, query: dict) -> model.Patient:
    mongo_delete: DeleteResultMongo = await model.Patient.delete(db, query)

    if mongo_delete.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Patient not found',
        )

    if not mongo_delete.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
