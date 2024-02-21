from typing import List, Optional

from sqlmodel import Field, Relationship

from src.core.database.base_crud import Base


class Potato(Base, table=True):
    id: int = Field(primary_key=True)
    name: str
    potato_collection_id: Optional[int] = Field(foreign_key="potatoes.id")


class Potatoes(Base, table=True):
    id: int = Field(primary_key=True)
    name: Optional[str]

    potatoes: List[Potato] = Relationship()
