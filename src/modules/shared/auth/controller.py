from fastapi import HTTPException, status
from jose import jwt, JWTError
from pydantic import ValidationError

from src.core.config import settings
from src.core.deps import DataBaseDep
from fastapi.security import OAuth2PasswordRequestForm
from src.core.utils.security import create_access_token, create_refresh_token
from src.modules.shared.auth import service
from src.modules.shared.auth.model import TokenSchema, TokenPayload, UserSecretCreate, UserSecretOut
from src.modules.shared.user.service import find_user_by_email, get_user_service


def root_controller():
    return service.root_service()


async def login_controller(db: DataBaseDep, form_data: OAuth2PasswordRequestForm) -> TokenSchema:
    user = await service.login_service(db, form_data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }


async def refresh_controller(db: DataBaseDep, refresh_token: str) -> TokenSchema:
    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    user = await get_user_service(db, {'id': token_data.sub})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token for user",
        )
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }


async def get_secret_and_qr(db, email) -> UserSecretOut:
    user = await find_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="That email does not exist in the system."
        )

    user_secret = service.generate_user_secret()
    qr_code = service.generate_qr_code(email, user_secret)

    result = await service.create_user_secret(
        db,
        UserSecretCreate(
            email=email, user_secret=user_secret, qr_code=qr_code)
    )

    return result
