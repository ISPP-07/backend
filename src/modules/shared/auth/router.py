from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.deps import DataBaseDep, get_current_user
from src.modules.shared.auth import controller
from src.modules.shared.auth import model
from src.modules.shared.user import model as user_model

router = APIRouter(tags=['Authentication'])


@router.get(
    '/master',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {'description': 'User not found'},
        status.HTTP_200_OK: {'description': 'Successful Response'}
    },
    response_model=model.UserIsMaster
)
async def is_master(
    user: Annotated[user_model.User, Depends(get_current_user)]
):
    return await controller.is_master_controller(user)


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=model.TokenSchema,
    responses={
        200: {"description": "Token successfully generated"},
        401: {"description": "Incorrect email or password"},
    }
)
async def login(
    db: DataBaseDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Authenticates a user and generates an access and refresh token.
    """
    return await controller.login_controller(db, form_data)


@router.post('/refresh',
             summary="Refresh token",
             response_model=model.TokenSchema,
             responses={
                 200: {"description": "Token successfully refreshed"},
                 403: {"description": "Invalid token"},
                 404: {"description": "Invalid token for user"},
             })
async def refresh_token(db: DataBaseDep, refresh_body: model.RefreshTokenBody):
    """
    Refreshes the access token using a refresh token.
    """
    return await controller.refresh_controller(db, refresh_token=refresh_body.refresh_token)


@router.post("/recovery-qr-code",
             response_model=model.UserSecretOut,
             responses={
                 200: {"description": "User secret and QR code generated successfully"},
                 400: {"description": "Email does not exist in the system"},
             })
async def get_secret_and_qr(db: DataBaseDep, user: user_model.User = Depends(get_current_user)):
    """
    Generates a new secret and QR code for a user, typically used for two-factor authentication
    setup.
    """
    email = user.email
    return await controller.get_secret_and_qr(db, email)
