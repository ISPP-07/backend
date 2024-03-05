from uuid import UUID
from pydantic import EmailStr, BaseModel

from src.core.database.base_crud import BaseMongo


class User(BaseMongo):
    id: UUID
    username: str
    password: str
    hashed_password: str
    email: EmailStr


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr
