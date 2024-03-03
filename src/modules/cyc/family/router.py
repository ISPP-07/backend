from typing import Any, List
from fastapi import APIRouter, status
from src.core.deps import SessionDep
from src.modules.cyc.family.controller import get_families_controller, create_family_controller
from src.modules.cyc.family.model import Family


router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK)
async def get_families(session: SessionDep) -> List[Family]:
    return await get_families_controller(session)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_family(session: SessionDep, family: Family) -> Family:
    return await create_family_controller(session, family)
