
from src.modules.shared.user import service
from src.modules.shared.user.schema import UserCreate


async def create_user_controller(session, user: UserCreate):
    return await service.create_user_service(session, user)
