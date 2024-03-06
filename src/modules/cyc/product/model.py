from typing import Optional
from pydantic import PositiveInt, FutureDate, UUID4, BaseModel

from src.core.database.base_crud import BaseMongo


class Product(BaseMongo):
    id: UUID4
    name: str
    quantity: PositiveInt
    exp_date: Optional[FutureDate]
    warehouses_id: list[UUID4]


class ProductCreate(BaseModel):
    name: str
    quantity: PositiveInt
    exp_date: Optional[FutureDate]
    warehouses_id: list[UUID4]


# WAREHOUSES TIENE QUE TENER LA LISTA CON TODAS LAS NUEVAS WAREHOUSES
class ProductUpdate(BaseModel):
    name: Optional[str]
    quantity: Optional[PositiveInt]
    exp_date: Optional[FutureDate]
    warehouses_id: Optional[list[UUID4]]


class Warehouse(BaseMongo):
    id: UUID4
    name: str
    products_id: list[UUID4]


class WarehouseCreate(BaseModel):
    name: str
    products_id: list[UUID4]
