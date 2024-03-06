from fastapi import APIRouter, Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.deps import DataBaseDep, get_current_user
from src.modules.shared.auth import controller
from src.modules.shared.auth.model import TokenSchema
from src.modules.shared.user.model import User, UserOut

router = APIRouter(
    tags=['core'],
)


@router.get('/')
def root():
    return controller.root_controller()


@router.post('/login', status_code=status.HTTP_200_OK, response_model=TokenSchema)
async def login(
    db: DataBaseDep,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    return await controller.login_controller(db, form_data)


@router.post('/test-token', response_model=UserOut)
async def test_token(user: User = Depends(get_current_user)):
    return user


@router.post('/refresh', summary="Refresh token", response_model=TokenSchema)
async def refresh_token(db: DataBaseDep, refresh_token: str = Body(...)):
    return await controller.refresh_controller(db, refresh_token)
