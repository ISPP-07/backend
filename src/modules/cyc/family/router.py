from typing import List
from fastapi import APIRouter
from fastapi import status
from src.modules.cyc.family.model import Family
from src.modules.cyc.family.controller import get_families_controller
from src.core.deps import SessionDep


router = APIRouter()


@router.get('/')
def root():
    return 'Hello cyc family router!'


@router.get('/list', status_code=status.HTTP_200_OK)
async def get_families(session: SessionDep) -> List[Family]:
    return await get_families_controller(session)
