from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.modules.cyc.family.model import Family, FamilyWithMembers
from src.modules.cyc.family import service


async def get_families_controller(db: DataBaseDep):
    return await service.get_families_service(db)


async def create_family_controller(db: DataBaseDep, family: Family):
    return await service.create_family_service(db, family)


async def get_family_details_controller(db: DataBaseDep, family_id: int):
    family = await service.get_family_service(db, query={'id': family_id})
    if family is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Family not found',
        )
    members = await service.get_family_members_service(db, family_id)
    result = FamilyWithMembers(**family.model_dump(), members=members)
    return result
