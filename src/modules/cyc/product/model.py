from typing import Optional
from uuid import UUID
from pydantic import PositiveInt, FutureDate

from src.core.database.base_crud import BaseMongo

# HAY QUE HACER UNA RELACION *-*


class Product(BaseMongo, table=True):
    id: UUID
    name: str
    quantity: PositiveInt
    exp_date: Optional[FutureDate]
    # warehouse_id: Optional[int] = Field(
    #     default=None, foreign_key='warehouse.id'
    # )
    # warehouse: 'Warehouse' = Relationship(back_populates='products')


class Warehouse(BaseMongo):
    id: UUID
    name: str
    # products: list[Product] = Relationship(back_populates='warehouse')
