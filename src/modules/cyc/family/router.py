from fastapi import APIRouter, status

from src.core.deps import DataBaseDep
from src.modules.cyc.family import controller
from src.modules.cyc.family.model import Family, FamilyWithMembers


router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[Family])
async def get_families(db: DataBaseDep):
    return await controller.get_families_controller(db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Family)
async def create_family(db: DataBaseDep, family: Family):
    return await controller.create_family_controller(db, family)


@router.get('/{family_id}', status_code=status.HTTP_200_OK, response_model=FamilyWithMembers)
async def get_family_details(db: DataBaseDep, family_id: int):
    return await controller.get_family_details_controller(db, family_id)
