from typing import Any
from fastapi import APIRouter

from src.core.deps import SessionDep

from src.modules.shared.root.controller import *
from src.modules.shared.root.model import Potato, Potatoes

router = APIRouter(
    tags=['core'],
)


@router.get('/')
def root():
    return root_controller()


@router.get('/potato/{potato_id}')
async def get_potato(session: SessionDep, potato_id: int) -> Any:
    return await get_potato_controller(session, potato_id)


@router.post('/potato')
async def create_potato(session: SessionDep, potato: Potato) -> Any:
    return await create_potato_controller(session, potato)
