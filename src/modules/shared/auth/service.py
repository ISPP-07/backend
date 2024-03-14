from fastapi import HTTPException, status
import pyotp
from src.core.database.mongo_types import InsertOneResultMongo
from src.core.deps import DataBaseDep
from src.core.utils.security import verify_password
from src.modules.shared.auth.model import UserSecret, UserSecretCreate, UserSecretOut
from src.modules.shared.user.model import User


def root_service():
    return 'Hello core auth router!'


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


async def login_service(db, form_data) -> User | None:
    user = await User.get(db, query={'username': form_data.username})
    if not (user and verify_password(form_data.password, user.password)):
        return None
    return user


async def create_user_secret(db: DataBaseDep, model: UserSecretCreate) -> UserSecretOut | None:
    user = await UserSecret.get(db, query={'email': model.email})
    if user:
        result = await UserSecret.update(db, {'email': model.email}, model.model_dump())
    else:
        insert_mongo: InsertOneResultMongo = await UserSecret.create(db, model.model_dump())
        if not insert_mongo.acknowledged:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='DB error'
            )
        result = await UserSecret.get(db, query={'id': insert_mongo.inserted_id})
    return result


async def get_secret_by_email(db: DataBaseDep, email: str) -> str:
    query = {'email': email}
    user = await UserSecret.get(db, query)
    return user.user_secret
