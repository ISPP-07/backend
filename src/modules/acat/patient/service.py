from typing import Any, Optional

from fastapi import HTTPException, status
from pydantic import UUID4

from src.core.database.base_crud import BulkOperation
from src.core.database.mongo_types import InsertOneResultMongo, DeleteResultMongo, UpdateResult, BulkWriteResult
from src.core.deps import DataBaseDep
from src.core.utils.helpers import get_all_combinations
from src.modules.acat.patient import model


async def get_patient_by_id(db: DataBaseDep, patient_id: UUID4) -> model.Patient | None:
    return await model.Patient.get(db, query={'id': patient_id})


async def get_patients_service(
    db: DataBaseDep,
    query: Optional[dict] = None,
    *args: Any,
    **kwargs: Any
) -> list[model.Patient]:
    query_combinations = get_all_combinations(args)
    query_parameters = None
    for combination in query_combinations:
        if any(c[1] is None for c in combination):
            continue
        query_parameters = {c[0]: c[1] for c in combination}
        date_queries = [c for c in combination if c[0] == 'registration_date']
        if len(date_queries) == 2:
            query_parameters['registration_date'] = dict(
                date_queries[0][1], **date_queries[1][1]
            )
    if query_parameters is not None:
        if query is None:
            query = {}
        query.update(query_parameters)
    return await model.Patient.get_multi(db, query, **kwargs)


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


async def bulk_service(db: DataBaseDep, operations: list[BulkOperation], **kwargs: Any):
    result: BulkWriteResult = await model.Patient.bulk_operation(
        db,
        [o.operation() for o in operations],
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


async def count_patients_service(db: DataBaseDep, query: dict) -> int:
    return await model.Patient.count(db, query)
