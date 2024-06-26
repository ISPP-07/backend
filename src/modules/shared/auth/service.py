import pyotp

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.database.mongo_types import DeleteResultMongo, InsertOneResultMongo
from src.core.deps import DataBaseDep
from src.core.utils.security import verify_password
from src.modules.shared.auth import model
from src.modules.shared.user import model as user_model


def generate_user_secret():
    secret = pyotp.random_base32()
    return secret


def generate_qr_code(email, secret):
    topt_object = pyotp.TOTP(secret)
    qr_text = topt_object.provisioning_uri(email, issuer_name="Harmony")
    return qr_text


def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)


async def login_service(db: DataBaseDep,
                        form_data: OAuth2PasswordRequestForm) -> user_model.User | None:
    user: user_model.User = await user_model.User.get(db, query={'username': form_data.username})
    if not (user and verify_password(form_data.password, user.password)):
        return None
    return user


async def create_user_secret(db: DataBaseDep, user_create: model.UserSecretCreate) -> model.UserSecretOut | None:
    user = await model.UserSecret.get(db, query={'email': user_create.email})
    if user:
        result = await model.UserSecret.update(db, {'email': user_create.email}, user_create.model_dump())
    else:
        insert_mongo: InsertOneResultMongo = await model.UserSecret.create(db, user_create.model_dump())
        if not insert_mongo.acknowledged:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='DB error'
            )
        result = await model.UserSecret.get(db, query={'id': insert_mongo.inserted_id})
    return result


async def get_secret_by_email(db: DataBaseDep, email: str) -> str:
    query = {'email': email}
    user = await model.UserSecret.get(db, query)
    return user.user_secret


async def store_refresh_token(db: DataBaseDep, rotation_token: model.RefreshTokenCreate) -> None:
    insert_mongo: InsertOneResultMongo = await model.RefreshToken.create(db, rotation_token.model_dump())
    if not insert_mongo.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )


async def get_refresh_token(db: DataBaseDep, user_id: str, refresh_token: str) -> model.RefreshToken | None:
    query = {'user_id': user_id, 'refresh_token': refresh_token}
    token = await model.RefreshToken.get(db, query)
    return token


async def update_refresh_token(db: DataBaseDep, token: model.RefreshToken) -> None:
    await model.RefreshToken.update(db, {'id': token.id}, data_to_update=token.model_dump())


async def delete_refresh_token(db: DataBaseDep, user_id: str) -> None:
    mongo_delete: DeleteResultMongo = await model.RefreshToken.delete(db, {'user_id': user_id})
    if mongo_delete.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Token not found'
        )
    if not mongo_delete.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
