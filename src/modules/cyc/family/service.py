from fastapi import HTTPException, status

from src.core.deps import AsyncIOMotorDatabase
from src.modules.cyc.family.model import Family, Person


async def get_families_service(db: AsyncIOMotorDatabase) -> list[Family]:
    return await Family.get_multi(db, query=None)


async def get_family_service(db: AsyncIOMotorDatabase, query: dict) -> Family | None:
    return await Family.get(db, query)


async def create_family_service(db: AsyncIOMotorDatabase, family: Family) -> Family:
    insert_mongo = await Family.create(db, obj_to_create=family.model_dump())
    if not insert_mongo.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    result = await get_family_service(db, query={'id': insert_mongo.inserted_id})
    return result


async def get_family_members_service(db, family_id: int) -> list[Person]:
    return await Person.get_multi(db, query={'family_id': family_id})
