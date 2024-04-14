from fastapi import HTTPException, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.core.config import settings
from src.modules.shared.user import model, service
from src.modules.shared.auth.service import get_secret_by_email, verify_otp


async def create_user_controller(
    db: DataBaseDep,
    user: model.UserCreate
) -> model.UserOut:
    new_user = user.model_dump()
    if settings.ACAT_NGO:
        new_user['master'] = True
    result = await service.create_user_service(db, new_user)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email or username already exist"
        )
    return result


async def create_user_master_controller(
    db: DataBaseDep,
    user: model.UserCreate
) -> model.UserOut:
    result = await service.create_user_service(db, {**user.model_dump(), 'master': True})
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email or username already exist"
        )
    return result


async def get_users_controller(db: DataBaseDep) -> list[model.User]:
    result = await service.get_users_service(db)
    return result


async def get_user_controller(db: DataBaseDep, user_id: UUID4) -> model.User:
    result = await service.get_user_service(db, query={'id': user_id})
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return result


async def update_user_controller(
    db: DataBaseDep,
    user_id: UUID4,
    user: model.UserUpdate
) -> model.UserOut:
    result = await service.update_user_service(db, query={'id': user_id}, user=user)
    if result == "Error 400":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exist"
        )
    if result == "Error 404":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return result


async def delete_user_controller(db: DataBaseDep, user_id: UUID4) -> None:
    await service.delete_user_service(db, user_id)


async def change_password_controller(
    otp_code: str,
    new_password: str,
    db: DataBaseDep,
    email: str
) -> dict:
    user = await service.find_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The email does not exist in the system.")
    secret = await get_secret_by_email(db, email)
    result = verify_otp(secret, otp_code)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The verification code is not valid. Please try again."
        )
    return await service.change_password_service(db, email, new_password)
