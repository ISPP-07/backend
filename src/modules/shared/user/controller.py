from fastapi import HTTPException, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.modules.shared.user.model import UserCreate, UserOut, UserUpdate
from src.modules.shared.user import service


async def create_user_controller(db: DataBaseDep, user: UserCreate) -> UserOut:
    result = await service.create_user_service(db, user)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exist"
        )
    return result


async def get_user_controller(db: DataBaseDep, user_id: UUID4) -> UserOut:
    result = await service.get_user_service(db, query={'id': user_id})
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return result


async def update_user_controller(db: DataBaseDep, user_id: UUID4, user: UserUpdate) -> UserOut:
    result = await service.update_user_service(db, query={'id': user_id}, user=user)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return result
