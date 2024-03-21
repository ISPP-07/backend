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
    user_db = await model.User.get(db, query)
    if user_db is None:
        return None
    hashed_password = get_hashed_password(user.password)
    user.password = hashed_password
    user_db = await model.User.update(
        db,
        query=query,
        data_to_update=user.model_dump()
    )
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
