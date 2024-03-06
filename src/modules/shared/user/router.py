from fastapi import APIRouter, status

from src.core.deps import DataBaseDep
from src.modules.shared.user.model import UserCreate, UserOut
from src.modules.shared.user.controller import create_user_controller

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(db: DataBaseDep, user: UserCreate):
    return await create_user_controller(db, user)
