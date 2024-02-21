from typing import Optional
from sqlmodel import Field

from src.core.database.base_crud import Base


class User(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    email: str
