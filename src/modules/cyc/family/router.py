from typing import List
from fastapi import APIRouter
from src.core.deps import SessionDep
from src.modules.cyc.family.controller import get_families_controller, create_family_controller
from src.modules.cyc.family.model import Family
from fastapi import status

router = APIRouter()


@router.get('/')
def root():
    return 'Hello cyc family router!'

@router.get('/list', status_code=status.HTTP_200_OK)
async def get_families(session: SessionDep) -> List[Family]:
    return await get_families_controller(session)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_family(session: SessionDep, family: Family) -> Family:
    return await create_family_controller(session, family)