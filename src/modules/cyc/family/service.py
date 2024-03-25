from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.core.database.mongo_types import InsertOneResultMongo, DeleteResultMongo
from src.modules.cyc.family.model import Family, FamilyCreate, FamilyUpdate


async def get_families_service(db: DataBaseDep) -> list[Family]:
    return await Family.get_multi(db)


async def get_family_service(db: DataBaseDep, query: dict) -> Family | None:
    return await Family.get(db, query)


async def create_family_service(
    db: DataBaseDep,
    family: FamilyCreate,
) -> InsertOneResultMongo:
    result = await Family.create(db, obj_to_create=family.model_dump())
    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    return result


async def update_family_service(
    db: DataBaseDep,
    query: dict,
    family: dict,
) -> Family:
    result = await Family.update(
        db,
        query=query,
        data_to_update=family
    )
    return result


async def delete_family_service(db: DataBaseDep, query: dict) -> Family:
    mongo_delete: DeleteResultMongo = await Family.delete(db, query)

    if mongo_delete.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Family not found',
        )

    if not mongo_delete.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
