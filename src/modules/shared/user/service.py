from sqlmodel import or_
from src.core.security import get_hashed_password
from src.modules.shared.user.model import User
from src.modules.shared.user.schema import UserCreate


async def create_user_service(session, user_in: UserCreate):
    user_check = await User.get_multi(session, or_(User.email == user_in.email, User.username == user_in.username))

    if len(user_check) > 0:
        return None

    hashed_password = get_hashed_password(user_in.password)
    user = await User.create(session, username=user_in.username, email=user_in.email, hashed_password=hashed_password)
    return user
