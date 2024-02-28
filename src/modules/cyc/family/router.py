from typing import Any
from fastapi import APIRouter
from src.core.deps import SessionDep
from src.modules.cyc.family.controller import create_family_controller
from src.modules.cyc.family.model import Family
from fastapi import status

router = APIRouter()


@router.get('/')
def root():
    return 'Hello cyc family router!'


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_family(session: SessionDep, family: Family) -> Any:
    return await create_family_controller(session, family)
