from fastapi import HTTPException, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.modules.shared.user import model, service


async def create_user_controller(db: DataBaseDep, user: model.UserCreate) -> model.UserOut:
    result = await service.create_user_service(db, user)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exist"
        )
    return result


async def get_user_controller(db: DataBaseDep, user_id: UUID4) -> model.UserOut:
    result = await service.get_user_service(db, query={'id': user_id})
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return result


async def update_user_controller(db: DataBaseDep, user_id: UUID4, user: model.UserUpdate) -> model.UserOut:
    result = await service.update_user_service(db, query={'id': user_id}, user=user)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return result


async def delete_user_controller(db: DataBaseDep, user_id: UUID4) -> None:
    await service.delete_user_service(db, user_id)
