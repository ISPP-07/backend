from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
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
