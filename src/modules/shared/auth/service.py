from src.core.utils.security import verify_password
from src.modules.shared.user.model import User


def root_service():
    return 'Hello core auth router!'


async def login_service(db, form_data) -> User | None:
    user = await User.get(db, query={'username': form_data.username})
    if not (user and verify_password(form_data.password, user.password)):
        return None
    return user
