from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from pydantic import ValidationError
from jose import jwt

from src.core.config import settings
from src.core.deps import SessionDep, get_current_user
from src.core.security import create_access_token, create_refresh_token, verify_password
from src.modules.shared.auth import controller
from src.modules.shared.auth.schema import TokenPayload, TokenSchema, UserAuth, UserOut
from src.modules.shared.user.model import User

router = APIRouter(
    tags=['core'],
)


@router.get('/')
def root():
    return controller.root_controller()


@router.get('/hello')
def hello():
    return controller.hello_controller()


@router.post('/login', response_model=TokenSchema)
async def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()) -> TokenSchema:
    user = await controller.login_controller(session, form_data)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }


@router.post('/test-token', response_model=UserOut)
async def test_token(user: User = Depends(get_current_user)) -> UserOut:
    return user


@router.post('/refresh', summary="Refresh token", response_model=TokenSchema)
async def refresh_token(session: SessionDep, refresh_token: str = Body(...)) -> TokenSchema:
    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[
                settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await User.get(session, id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token for user",
        )
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }
