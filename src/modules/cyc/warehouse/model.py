from typing import Optional
from pydantic import PositiveInt, FutureDate, UUID4, BaseModel, field_validator, ValidationError

from src.core.database.base_crud import BaseMongo


class Product(BaseModel):
    name: str
    quantity: PositiveInt
    exp_date: Optional[FutureDate]


class ProductOut(Product):
    warehouse_id: UUID4


class ProductCreate(Product):
    warehouses_id: list[UUID4]


class ProductUpdate(Product):
    warehouses_id: list[UUID4]
    name: str
    quantity: Optional[PositiveInt]
    exp_date: Optional[FutureDate]


class Warehouse(BaseMongo):
    id: UUID4
    name: str
    products: list[Product]


class WarehouseCreate(BaseModel):
    name: str
    products: list[Product]

    # @field_validator('products', mode='after')
    # @classmethod
    # def validate_products(cls, v: list[Product]):
    #     if len(set(p.name for p in v)) != len(v):
    #         ValidationError({
    #             'field': 'products',
    #             'msg': 'Duplicated products'
    #         })


class WarehouseUpdate(BaseModel):
    name: Optional[str]
    products: Optional[list[Product]]

    # @field_validator('products', mode='after')
    # @classmethod
    # def validate_products(cls, v: list[Product]):
    #     if len(set(p.name for p in v)) != len(v):
    #         ValidationError({
    #             'field': 'products',
    #             'msg': 'Duplicated products'
    #         })
