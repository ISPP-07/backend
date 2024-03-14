from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.modules.shared.auth.service import get_secret_by_email, verify_otp
from src.modules.shared.user.model import UserCreate, UserOut
from src.modules.shared.user import service


async def create_user_controller(db: DataBaseDep, user: UserCreate) -> UserOut:
    result = await service.create_user_service(db, user)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exist"
        )
    return result


async def change_password_controller(
        otp_code: str, new_password: str, db: DataBaseDep, email: str) -> dict:
    user = await service.find_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico introducido no está asociado a ningún usuario"
        )
    secret = await get_secret_by_email(db, email)
    result = verify_otp(secret, otp_code)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El código de verificación es incorrecto"
        )
    return await service.change_password_service(db, email, new_password)
