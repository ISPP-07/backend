from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.core.database.mongo_types import InsertOneResultMongo
from src.modules.cyc.family.model import Family, FamilyCreate


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
