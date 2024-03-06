from pydantic import BaseModel, UUID4


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: UUID4 = None
    exp: int = None


class UserAuth(BaseModel):
    username: str
    password: str
