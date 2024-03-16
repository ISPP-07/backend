from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.core.utils.security import get_hashed_password
from src.core.database.mongo_types import InsertOneResultMongo
from src.modules.shared.user.model import UserCreate, User, UserOut


async def get_user_service(db: DataBaseDep, query: dict) -> User:
    return await User.get(db, query)


async def create_user_service(db: DataBaseDep, user: UserCreate) -> UserOut | None:
    user_check = await User.get_multi(
        db,
        query={'$or': [{'username': user.username}, {'email': user.email}]},
    )
    if len(user_check) > 0:
        return None
    hashed_password = get_hashed_password(user.password)
    user.password = hashed_password
    insert_mongo: InsertOneResultMongo = await User.create(db, user.model_dump())
    if not insert_mongo.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    user_db = await User.get(db, query={'id': insert_mongo.inserted_id})
    result = UserOut(
        id=user_db.id,
        username=user_db.username,
        email=user_db.email
    )
    return result


async def find_user_by_email(db: DataBaseDep, email: str) -> User:
    query = {'email': email}
    user = await User.get(db, query)
    return user


async def find_username_by_email(db: DataBaseDep, email: str) -> str:
    query = {'email': email}
    user = await User.get(db, query)
    if user:
        return user.username
    else:
        return None


async def change_password_service(db: DataBaseDep, email: str, new_password: str) -> dict:
    hashed_password = get_hashed_password(new_password)
    await User.update(db, {'email': email}, {'password': hashed_password})
    return {'detail': 'Your password has been changed successfully.'}
