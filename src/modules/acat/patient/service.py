from typing import Any
from uuid import uuid4

from fastapi import HTTPException, status
from pydantic import UUID4
from pymongo import InsertOne, UpdateOne, UpdateMany

from src.core.database.mongo_types import InsertOneResultMongo, DeleteResultMongo, UpdateResult, BulkWriteResult
from src.core.deps import DataBaseDep
from src.modules.acat.patient import model


async def get_patient_by_id(db: DataBaseDep, patient_id: UUID4) -> model.Patient | None:
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


async def update_many_patient_service(
    db: DataBaseDep,
    query: dict,
    update: dict,
    **kwargs
) -> UpdateResult:
    return await model.Patient.update_many(
        db=db,
        query=query,
        data_to_update=update,
        **kwargs
    )


async def bulk_create_service(
    db: DataBaseDep,
    patients: list[model.PatientCreate],
    **kwargs: Any,
) -> BulkWriteResult:
    result: BulkWriteResult = await model.Patient.bulk_operation(
        db,
        [
            InsertOne(model.Patient(**p.model_dump(), id=uuid4()).mongo())
            for p in patients
        ],
        **kwargs
    )
    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    return result


async def bulk_update_service(
    db: DataBaseDep,
    query_and_data: list[tuple[dict, dict]],
    many: bool = False,
    **kwargs: Any
) -> BulkWriteResult:
    operations = []
    for (query, data) in query_and_data:
        if not many:
            operations.append(UpdateOne(filter=query, update=data))
        else:
            operations.append(UpdateMany(filter=query, update=data))
    result: BulkWriteResult = await model.Patient.bulk_operation(
        db,
        operations,
        **kwargs
    )
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


async def update_patient_service(
    db: DataBaseDep,
    query: dict,
    updated_patient_data: dict,
    **kwargs: Any
) -> model.Patient | None:
    return await model.Patient.update(
        db,
        query=query,
        data_to_update=updated_patient_data,
        **kwargs
    )


async def delete_patient_service(db: DataBaseDep, query: dict) -> model.Patient:
    mongo_delete: DeleteResultMongo = await model.Patient.delete(db, query)
    if not mongo_delete.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    if mongo_delete.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Patient not found',
        )
