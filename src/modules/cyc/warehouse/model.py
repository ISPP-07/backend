from uuid import uuid4
from typing import Optional

from pydantic import PositiveInt, FutureDate, UUID4, BaseModel

from src.core.database.base_crud import BaseMongo


class Product(BaseModel):
    id: UUID4 = uuid4()
    name: str
    quantity: PositiveInt
    exp_date: Optional[FutureDate] = None


class ProductOut(Product):
    warehouse_id: UUID4


class WarehouseProductCreate(BaseModel):
    name: str
    exp_date: Optional[FutureDate] = None
    quantity: PositiveInt
    warehouse_id: UUID4


class WarehouseProductUpdate(BaseModel):
    name: Optional[str] = None
    exp_date: Optional[FutureDate] = None
    quantity: Optional[PositiveInt] = None
    update_exp_date: bool = False
    warehouse_id: UUID4
    product_id: UUID4


class ProductCreate(BaseModel):
    products: list[WarehouseProductCreate]


class ProductUpdate(BaseModel):
    products: list[WarehouseProductUpdate]


class Warehouse(BaseMongo):
    id: UUID4
    name: str
    products: list[Product]


class WarehouseCreate(BaseModel):
    name: str
    products: list[Product]


class WarehouseUpdate(BaseModel):
    name: Optional[str] = None
    products: list[Product] = []
