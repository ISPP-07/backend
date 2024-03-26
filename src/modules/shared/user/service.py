from fastapi import HTTPException, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.core.utils.security import get_hashed_password
from src.core.database.mongo_types import InsertOneResultMongo, DeleteResultMongo
from src.modules.shared.user import model


async def get_user_service(db: DataBaseDep, query: dict) -> model.UserOut | None:
    return await model.User.get(db, query)


async def create_user_service(db: DataBaseDep, user: model.UserCreate) -> model.UserOut | None:
    user_check = await model.User.get_multi(
        db,
        query={'$or': [{'username': user.username}, {'email': user.email}]},
    )
    if len(user_check) > 0:
        return None
    hashed_password = get_hashed_password(user.password)
    user.password = hashed_password
    insert_mongo: InsertOneResultMongo = await model.User.create(db, user.model_dump())
    if not insert_mongo.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    user_db = await model.User.get(db, query={'id': insert_mongo.inserted_id})
    result = model.UserOut(
        id=user_db.id,
        username=user_db.username,
        email=user_db.email
    )
    return result


async def update_user_service(db: DataBaseDep, query: dict, user: model.UserUpdate) -> model.UserOut | None:
    if user.password:
        hashed_password = get_hashed_password(user.password)
        user.password = hashed_password

    user_db: model.User | None = await model.User.update(db, query, user.model_dump())
    if user_db is None:
        return None

    result = model.UserOut(
        id=user_db.id,
        username=user_db.username,
        email=user_db.email
    )
    return result


async def delete_user_service(db: DataBaseDep, user_id: UUID4) -> None:
    mongo_delete: DeleteResultMongo = await model.User.delete(db, query={'id': user_id})

    if mongo_delete.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    if not mongo_delete.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )


async def find_user_by_email(db: DataBaseDep, email: str) -> model.User:
    query = {'email': email}
    user = await model.User.get(db, query)
    return user


async def find_username_by_email(db: DataBaseDep, email: str) -> str:
    query = {'email': email}
    user = await model.User.get(db, query)
    if user:
        return user.username
    else:
        return None


async def change_password_service(db: DataBaseDep, email: str, new_password: str) -> dict:
    hashed_password = get_hashed_password(new_password)
    await model.User.update(db, {'email': email}, {'password': hashed_password})
    return {'detail': 'Your password has been changed successfully.'}
