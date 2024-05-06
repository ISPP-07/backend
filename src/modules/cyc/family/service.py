from typing import Any

from pydantic import UUID4
from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.core.database.base_crud import BulkOperation
from src.core.utils.helpers import get_all_combinations
from src.core.database.mongo_types import InsertOneResultMongo, DeleteResultMongo, BulkWriteResult
from src.modules.cyc.family import model


async def get_families_service(
    db: DataBaseDep,
    *args: Any,
    **kwargs: Any
) -> list[model.Family]:
    query_combinations = get_all_combinations(args)
    query = None
    for combination in query_combinations:
        if any(c[1] is None for c in combination):
            continue
        query = {c[0]: c[1] for c in combination}
    return await model.Family.get_multi(db=db, query=query, **kwargs)


async def get_members_service(db: DataBaseDep, query: dict = None) -> list[model.Person]:
    families: list[model.Family] = await model.Family.get_multi(db, query)
    result = [member for family in families for member in family.members]
    return result


async def get_family_service(db: DataBaseDep, query: dict) -> model.Family | None:
    return await model.Family.get(db, query)


async def create_family_service(
    db: DataBaseDep,
    family: dict,
) -> InsertOneResultMongo:
    result = await model.Family.create(db, obj_to_create=family)
    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    return result


async def delete_family_service(db: DataBaseDep, query: dict) -> model.Family:
    mongo_delete: DeleteResultMongo = await model.Family.delete(db, query)

    if mongo_delete.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Family not found'
        )
    if not mongo_delete.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )


async def update_family_service(
    db: DataBaseDep,
    family_id: UUID4,
    family_update: dict
) -> model.Family | None:
    return await model.Family.update(
        db,
        query={'id': family_id},
        data_to_update=family_update
    )


async def count_families_service(db: DataBaseDep, query: dict) -> int:
    return await model.Family.count(db, query)


async def bulk_service(db: DataBaseDep, operations: list[BulkOperation], **kwargs: Any):
    result: BulkWriteResult = await model.Family.bulk_operation(
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
