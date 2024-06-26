from typing import Optional
from datetime import date
from pydantic import PositiveInt, FutureDate, UUID4, BaseModel, NonNegativeInt

from src.core.database.base_crud import BaseMongo


class Product(BaseModel):
    id: UUID4
    name: str
    quantity: NonNegativeInt
    exp_date: Optional[date] = None


class ProductWithoutId(BaseModel):
    name: str
    quantity: NonNegativeInt
    exp_date: Optional[date] = None


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
    products: list[ProductWithoutId]


class WarehouseUpdate(BaseModel):
    name: Optional[str] = None
    products: list[Product] = None


class GetProducts(BaseModel):
    elements: list[ProductOut]
    total_elements: NonNegativeInt
