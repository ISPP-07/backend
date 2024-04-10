from pydantic import ValidationError
from jose import jwt, JWTError

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.config import settings
from src.core.deps import DataBaseDep
from src.core.utils.security import create_access_token, create_refresh_token
from src.modules.shared.auth import service
from src.modules.shared.auth import model
from src.modules.shared.user import model as user_model
from src.modules.shared.user import service as user_service


async def login_controller(db: DataBaseDep, form_data: OAuth2PasswordRequestForm) -> model.TokenSchema:
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
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    user = await user_service.get_user_service(db, {'id': token_data.sub})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token for user",
        )
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }


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
