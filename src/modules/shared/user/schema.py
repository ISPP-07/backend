from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    email: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
