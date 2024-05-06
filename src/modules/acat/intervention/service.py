from typing import Any

from fastapi import HTTPException, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.core.database.base_crud import BulkOperation
from src.core.database.mongo_types import DeleteResultMongo, InsertOneResultMongo, UpdateResult, BulkWriteResult
from src.core.utils.helpers import get_all_combinations
from src.modules.acat.intervention import model
from src.modules.acat.patient import model as patient_model


async def get_intervention_service(db: DataBaseDep, query: dict) -> model.Intervention | None:
    intervention = await model.Intervention.get(db, query)
    if not intervention:
        return None
    return intervention


async def get_interventions_service(
    db: DataBaseDep,
    *args: Any,
    **kwargs: Any
) -> list[model.Intervention]:
    query_combinations = get_all_combinations(args)
    query: dict = None
    for combination in query_combinations:
        if any(c[1] is None for c in combination):
            continue
        query = {c[0]: c[1] for c in combination}
        date_queries = [c for c in combination if c[0] == 'date']
        if len(date_queries) == 2:
            query['date'] = dict(
                date_queries[0][1], **date_queries[1][1]
            )
    return await model.Intervention.get_multi(db, query=query, **kwargs)


async def create_intervention_service(
    db: DataBaseDep,
    intervention_data: model.InterventionCreate,
    patient_data: patient_model.Patient
) -> InsertOneResultMongo:
    intervention_dict = intervention_data.model_dump()
    intervention_dict['patient'] = patient_data.model_dump()
    intervention_dict.pop('patient_id')

    result: InsertOneResultMongo = await model.Intervention.create(db, obj_to_create=intervention_dict)

    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    return result


async def update_intervention_service(
    db: DataBaseDep,
    intervention_id: UUID4,
    updated_intervention_data: dict,
) -> model.Intervention | None:
    return await model.Intervention.update(
        db,
        query={'id': intervention_id},
        data_to_update=updated_intervention_data
    )


async def update_interventions_service(
    db: DataBaseDep,
    query: dict,
    updated_intervention_data: dict,
) -> UpdateResult:
    return await model.Intervention.update_many(
        db,
        query,
        data_to_update=updated_intervention_data
    )


async def bulk_service(db: DataBaseDep, operations: list[BulkOperation], **kwargs: Any):
    result: BulkWriteResult = await model.Intervention.bulk_operation(
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


async def delete_intervention_service(db: DataBaseDep, query: dict) -> model.Intervention:
    mongo_delete: DeleteResultMongo = await model.Intervention.delete(db, query)

    if not mongo_delete.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )

    if mongo_delete.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Intervention not found',
        )


async def count_interventions_service(db: DataBaseDep, query: dict) -> int:
    return await model.Intervention.count(db, query)
