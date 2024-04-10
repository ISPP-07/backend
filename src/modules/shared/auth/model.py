from pydantic import BaseModel, UUID4, EmailStr

from src.core.database.base_crud import BaseMongo


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: UUID4 = None
    exp: int = None
    scopes: list[str] = []


class UserAuth(BaseModel):
    username: str
    password: str


class UserSecret(BaseMongo):
    id: UUID4
    email: EmailStr
    user_secret: str
    qr_code: str


class UserSecretCreate(BaseModel):
    email: EmailStr
    user_secret: str
    qr_code: str


class UserSecretOut(BaseModel):
    email: EmailStr
    qr_code: str


class RefreshTokenBody(BaseModel):
    refresh_token: str
