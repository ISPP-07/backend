from typing import Optional
from datetime import date
from sqlmodel import Field, Relationship
from pydantic import PositiveInt

from src.core.database.base_crud import Base

# POR AHORA LO HE RELACIONADO COMO 1-* PERO PODRIA SER *-*
# SI UN MISMO PRODUCTO LO GUARDAN EN ALMACENES DIFERENTES


class Product(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    quantity: PositiveInt
    exp_date: Optional[date]
    warehouse_id: Optional[int] = Field(
        default=None, foreign_key='warehouse.id'
    )
    warehouse: 'Warehouse' = Relationship(back_populates='products')


class Warehouse(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    products: list[Product] = Relationship(back_populates='warehouse')
