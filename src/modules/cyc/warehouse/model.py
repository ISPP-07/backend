from uuid import uuid4
from typing import Optional

from pydantic import PositiveInt, FutureDate, UUID4, BaseModel

from src.core.database.base_crud import BaseMongo


class Product(BaseModel):
    id: UUID4 = uuid4()
    name: str = None
    quantity: PositiveInt
    exp_date: Optional[FutureDate] = None


class ProductOut(Product):
    warehouse_id: UUID4


class WarehouseProductCreate(BaseModel):
    warehouse_id: UUID4
    quantity: PositiveInt


class WarehouseProductUpdate(WarehouseProductCreate):
    product_id: UUID4 = None


class ProductCreate(BaseModel):
    name: str
    exp_date: Optional[FutureDate] = None
    warehouses: list[WarehouseProductCreate]


class ProductUpdate(BaseModel):
    name: str = None
    exp_date: Optional[FutureDate] = None
    warehouses: list[WarehouseProductUpdate] = []


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
