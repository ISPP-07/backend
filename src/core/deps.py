from collections.abc import AsyncGenerator
from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import ValidationError
from jose import jwt, JWTError

from src.core.database.session import get_client
from src.core.config import settings
from src.modules.shared.auth import model as auth_model
from src.modules.shared.user import model as user_model


reusable_oauth = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_STR}shared/auth/login",
    scheme_name="JWT",
)


async def get_db() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    client_db = get_client()
    db = client_db.get_database(settings.MONGO_DB)
    yield db

DataBaseDep = Annotated[AsyncIOMotorDatabase, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth)]


async def get_current_user(db: DataBaseDep, token: TokenDep) -> user_model.User:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = auth_model.TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    user = await user_model.User.get(db, {'id': token_data.sub})

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user


async def get_master_user(
    user: Annotated[user_model.User, Depends(get_current_user)]
) -> user_model.User:
    if not user.master:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough privileges',
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
