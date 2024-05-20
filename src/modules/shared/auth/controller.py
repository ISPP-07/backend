from datetime import datetime, timedelta, timezone
import pytz
from pydantic import ValidationError
from jose import jwt, JWTError

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.config import settings
from src.core.deps import DataBaseDep
from src.core.utils.security import create_access_token, create_refresh_token
from src.modules.shared.auth import service, model
from src.modules.shared.user import model as user_model, service as user_service


async def login_controller(db: DataBaseDep, form_data: OAuth2PasswordRequestForm) -> model.TokenSchema:
    user = await service.login_service(db, form_data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    rotation_token = model.RefreshTokenCreate(
        user_id=user.id,
        refresh_token=refresh_token,
        expires_at=datetime.now(timezone.utc) + timedelta(
            seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS
        )
    )
    await service.store_refresh_token(db, rotation_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


async def refresh_controller(db: DataBaseDep, refresh_token: str) -> model.TokenSchema:
    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        token_data = model.TokenPayload(**payload)
    except (JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    stored_token = await service.get_refresh_token(db, token_data.sub, refresh_token)
    if stored_token:
        if not stored_token.is_valid() or stored_token.used:
            await service.delete_refresh_token(db, token_data.sub)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        stored_token.used = True
        await service.update_refresh_token(db, stored_token)

        access_token = create_access_token(token_data.sub)
        refresh_token = create_refresh_token(token_data.sub)

        rotation_token = model.RefreshTokenCreate(
            user_id=token_data.sub,
            refresh_token=refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(
                seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS
            )
        )
        await service.store_refresh_token(db, rotation_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_secret_and_qr(db, email) -> model.UserSecretOut:
    user = await user_service.find_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="That email does not exist in the system."
        )

    user_secret = service.generate_user_secret()
    qr_code = service.generate_qr_code(email, user_secret)

    result = await service.create_user_secret(
        db,
        model.UserSecretCreate(
            email=email, user_secret=user_secret, qr_code=qr_code)
    )

    return result


async def is_master_controller(
    user: user_model.User
) -> model.UserIsMaster:
    return model.UserIsMaster(
        id=user.id,
        is_master=user.master
    )
