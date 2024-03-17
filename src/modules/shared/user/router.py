from pydantic import EmailStr

from fastapi import APIRouter, status

from src.core.deps import DataBaseDep
from src.modules.shared.user import controller
from src.modules.shared.user import model

router = APIRouter(tags=['User'])


@router.post('/',
             status_code=status.HTTP_201_CREATED,
             response_model=model.UserOut,
             responses={
                 201: {"description": "User successfully created"},
                 400: {"description": "User with this email or username already exists"},
             })
async def create_user(db: DataBaseDep, user: model.UserCreate):
    """
    Creates a new user with the provided details.
    """
    return await controller.create_user_controller(db, user)


@router.post('/change-password',
             status_code=status.HTTP_200_OK,
             responses={
                 200: {"description": "Password successfully changed"},
                 400: {
                     "description": "Email does not exist in the system or The verification code"
                     + " is not valid"
                 },
             })
async def change_password(
        email: EmailStr,
        otp_code: str,
        new_password: str,
        db: DataBaseDep) -> dict:
    """
    Changes the password for a user identified by email, using a one-time password (OTP) 
    for verification.
    """
    return await controller.change_password_controller(otp_code, new_password, db, email)
