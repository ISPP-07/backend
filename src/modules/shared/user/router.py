from pydantic import EmailStr
from typing import Annotated

from fastapi import APIRouter, status, Depends
from pydantic import UUID4

from src.core.deps import DataBaseDep, get_current_user, get_master_user
from src.server import dependencies
from src.modules.shared.user import model
from src.modules.shared.user import controller

router = APIRouter(tags=['User'], dependencies=dependencies)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"description": "User already exists"},
        status.HTTP_201_CREATED: {"description": "User created"}
    },
    response_model=model.UserOut,
    dependencies=[Depends(get_master_user)]
)
async def create_user(
    db: DataBaseDep,
    user: model.UserCreate,
):
    '''
    Create a new user
    '''
    return await controller.create_user_controller(db, user)


@router.post(
    '/master',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {'description': 'User already exists'},
        status.HTTP_201_CREATED: {'description': 'User created'}
    },
    response_model=model.UserOut,
    dependencies=[Depends(get_master_user)]
)
async def create_user_master(
    db: DataBaseDep,
    user: model.UserCreate,
):
    return await controller.create_user_master_controller(db, user)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Successful Response"}
    },
    response_model=list[model.UserOut]
)
async def get_users(db: DataBaseDep):
    '''
    Get all users
    '''
    return await controller.get_users_controller(db)


@router.get(
    '/me',
    response_model=model.UserOut,
    responses={
        200: {"description": "User information retrieved successfully"},
    }
)
async def get_me(user: Annotated[model.User, Depends(get_current_user)]):
    return user


@router.get(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Successful Response"}
    },
    response_model=model.UserOut
)
async def get_user_details(db: DataBaseDep, user_id: UUID4):
    '''
    Get user by id
    '''
    return await controller.get_user_controller(db, user_id)


@router.patch(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
        status.HTTP_200_OK: {"description": "User updated"}
    },
    response_model=model.UserOut,
    dependencies=[Depends(get_master_user)]
)
async def update_user(db: DataBaseDep, user_id: UUID4, user: model.UserUpdate):
    '''
    Update user by id
    '''
    return await controller.update_user_controller(db, user_id, user)


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
        status.HTTP_204_NO_CONTENT: {"description": "User deleted"}
    },
    response_model=None,
    dependencies=[Depends(get_master_user)]
)
async def delete_user(
    db: DataBaseDep,
    user_id: UUID4,
):
    '''
    Delete user by id
    '''
    await controller.delete_user_controller(db, user_id)
    return None


@router.post(
    '/change-password',
    status_code=status.HTTP_200_OK,
    response_model=dict,
    responses={
        200: {
            "description": "Password successfully changed"
        },
        400: {
            "description": "Email does not exist in the system or The verification code" +
            " is not valid"
        },
    }
)
async def change_password(
        email: EmailStr,
        otp_code: str,
        new_password: str,
        db: DataBaseDep
):
    """
    Changes the password for a user identified by email, using a one-time password (OTP)
    for verification.
    """
    return await controller.change_password_controller(otp_code, new_password, db, email)
