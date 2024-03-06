from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.modules.cyc.family.model import Family, FamilyCreate
from src.modules.cyc.family import service


async def get_families_controller(db: DataBaseDep):
    return await service.get_families_service(db)


async def create_family_controller(db: DataBaseDep, family: FamilyCreate) -> Family:
    mongo_insert = await service.create_family_service(db, family)
    result = await service.get_family_service(db, query={'id': mongo_insert.inserted_id})
    return result


async def get_family_details_controller(db: DataBaseDep, family_id: int) -> Family:
    result = await service.get_family_service(db, query={'id': family_id})
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Family not found',
        )
    return result
