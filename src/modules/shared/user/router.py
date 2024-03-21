from fastapi import APIRouter, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.modules.shared.user import model
from src.modules.shared.user import controller

router = APIRouter()


@router.post('/', 
             status_code=status.HTTP_201_CREATED, 
             responses={
                 status.HTTP_409_CONFLICT: {"description": "User already exists"},
                 status.HTTP_201_CREATED: {"description": "User created"}
             },
             response_model=model.UserOut)
async def create_user(db: DataBaseDep, user: model.UserCreate):
    '''
    Create a new user
    '''
    return await controller.create_user_controller(db, user)


@router.get('/{user_id}',
            status_code=status.HTTP_200_OK, 
            responses={
                status.HTTP_404_NOT_FOUND: {"description": "User not found"},
                status.HTTP_200_OK: {"description": "User found"}
            },
            response_model=model.UserOut)
async def get_user(db: DataBaseDep, user_id: UUID4):
    '''
    Get user by id
    '''
    return await controller.get_user_controller(db, user_id)


@router.patch('/{user_id}', 
              status_code=status.HTTP_200_OK, 
              responses={
                  status.HTTP_404_NOT_FOUND: {"description": "User not found"},
                  status.HTTP_200_OK: {"description": "User updated"}
            },
              response_model=model.UserOut)
async def update_user(db: DataBaseDep, user_id: UUID4, user: model.UserUpdate):
    '''
    Update user by id
    '''
    return await controller.update_user_controller(db, user_id, user)


@router.delete('/{user_id}', 
               status_code=status.HTTP_204_NO_CONTENT, 
               responses={
                     status.HTTP_404_NOT_FOUND: {"description": "User not found"},
                     status.HTTP_204_NO_CONTENT: {"description": "User deleted"}
                },
               response_model=None)
async def delete_user(db: DataBaseDep, user_id: UUID4):
    '''
    Delete user by id
    '''
    await controller.delete_user_controller(db, user_id)
    return None
