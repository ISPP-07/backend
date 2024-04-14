from pydantic import EmailStr, BaseModel, UUID4
from typing import Optional

from src.core.database.base_crud import BaseMongo


class User(BaseMongo):
    id: UUID4
    master: bool = False
    username: str
    password: str
    email: EmailStr


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserOut(BaseModel):
    id: UUID4
    username: str
    email: EmailStr


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
