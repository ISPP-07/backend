from typing import Optional

from fastapi import HTTPException, status
from pydantic import PositiveInt, FutureDate, UUID4, BaseModel, field_validator

from src.core.database.base_crud import BaseMongo


# TENEMOS QUE DIFERENCIAR POR LOTES, DONDE UN MISMO PRODUCTO PUEDE TENER DIFERENTES FECHAS DE CADUCIDAD
class Product(BaseModel):
    name: str
    quantity: PositiveInt
    exp_date: Optional[FutureDate] = None


class ProductOut(Product):
    warehouse_id: UUID4


class WarehouseProductCreate(BaseModel):
    warehouse_id: UUID4
    quantity: PositiveInt


class ProductCreate(BaseModel):
    name: str
    exp_date: Optional[FutureDate] = None
    warehouses: list[WarehouseProductCreate]


class ProductUpdate(BaseModel):
    name: str
    exp_date: Optional[FutureDate] = None
    warehouses: list[WarehouseProductCreate] = []


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
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail={
    #                 'field': 'products',
    #                 'msg': 'Duplicated products'
    #             }
    #         )


class WarehouseUpdate(BaseModel):
    name: Optional[str] = None
    products: list[Product] = []
