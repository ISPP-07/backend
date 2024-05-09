from datetime import datetime
import pytz
from pydantic import BaseModel, UUID4, EmailStr

from src.core.database.base_crud import BaseMongo


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: UUID4 = None
    exp: int = None


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


class UserIsMaster(BaseModel):
    id: UUID4
    is_master: bool


class RefreshToken(BaseMongo):
    id: UUID4
    user_id: UUID4
    refresh_token: str
    expires_at: datetime
    used: bool = False

    def is_valid(self):
        return self.expires_at > datetime.now(pytz.utc) and not self.used


class RefreshTokenCreate(BaseModel):
    user_id: UUID4
    refresh_token: str
    expires_at: datetime
    used: bool = False
