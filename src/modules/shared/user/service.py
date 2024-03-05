from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.core.security import get_hashed_password
from src.core.database.mongo_types import InsertOneResultMongo
from src.modules.shared.user.model import UserCreate, User, UserOut


async def get_user_service(db: DataBaseDep, session, query: dict) -> User:
    return await User.get(db, query, session=session)


async def create_user_service(db: DataBaseDep, session, user: UserCreate) -> UserOut | None:
    user_check = await User.get_multi(
        db,
        {'$or': [{'username': user.username}, {'email': user.email}]},
        session=session,
    )
    if len(user_check) > 0:
        return None
    hashed_password = get_hashed_password(user.password)
    user.password = hashed_password
    insert_mongo: InsertOneResultMongo = await User.create(db, user.model_dump(), session=session)
    if not insert_mongo.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    user_db = await get_user_service(db, session, {'id': insert_mongo.inserted_id})
    result = UserOut(
        id=user_db.id,
        username=user_db.username,
        email=user_db.email
    )
    return result
