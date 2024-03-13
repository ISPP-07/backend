from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.deps import DataBaseDep, get_current_user
from src.modules.shared.auth import controller
from src.modules.shared.auth.model import TokenSchema, RefreshTokenBody
from src.modules.shared.user.model import User, UserOut

router = APIRouter(
    tags=['core'],
)


@router.get('/')
def root():
    return controller.root_controller()


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=TokenSchema,
)
async def login(
    db: DataBaseDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return await controller.login_controller(db, form_data)


@router.post('/test-token', response_model=UserOut)
async def test_token(user: Annotated[User, Depends(get_current_user)]):
    return user


@router.post('/refresh', summary="Refresh token", response_model=TokenSchema)
async def refresh_token(db: DataBaseDep, refresh_body: RefreshTokenBody):
    return await controller.refresh_controller(db, refresh_token=refresh_body.refresh_token)
