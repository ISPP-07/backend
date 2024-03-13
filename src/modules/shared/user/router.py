from fastapi import APIRouter, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.modules.shared.user.model import UserCreate, UserOut, UserUpdate
from src.modules.shared.user.controller import create_user_controller, get_user_controller, update_user_controller, delete_user_controller

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(db: DataBaseDep, user: UserCreate):
    return await create_user_controller(db, user)


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_user(db: DataBaseDep, user_id: UUID4):
    return await get_user_controller(db, user_id)


@router.patch('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserOut)
async def update_user(db: DataBaseDep, user_id: UUID4, user: UserUpdate):
    return await update_user_controller(db, user_id, user)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_user(db: DataBaseDep, user_id: UUID4):
    await delete_user_controller(db, user_id)
    return None
