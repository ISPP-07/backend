from src.core.deps import DataBaseDep
from src.modules.shared.user.model import UserCreate, UserOut
from src.modules.shared.user import service


async def create_user_controller(db: DataBaseDep, session, user: UserCreate) -> UserOut:
    return await service.create_user_service(db, session, user)
