from fastapi import APIRouter, status
from pydantic import EmailStr

from src.core.deps import DataBaseDep
from src.modules.shared.user import controller
from src.modules.shared.user.model import UserCreate, UserOut
from src.modules.shared.user.controller import create_user_controller

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(db: DataBaseDep, user: UserCreate):
    return await create_user_controller(db, user)


@router.post('/change-password', status_code=status.HTTP_200_OK)
async def change_password(
        email: EmailStr,
        otp_code: str,
        new_password: str,
        db: DataBaseDep) -> dict:

    return await controller.change_password_controller(otp_code, new_password, db, email)
