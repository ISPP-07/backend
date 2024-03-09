from typing import Optional
from datetime import date
from pydantic import BaseModel, UUID4, PositiveInt
from src.core.database.base_crud import BaseMongo
from src.modules.cyc.warehouse.model import Product


class Delivery(BaseMongo):
    id: UUID4
    date: date
    months: PositiveInt
    products: list[Product]


class DeliveryCreate(BaseModel):
    date: date
    months: PositiveInt
    products: list[Product]


class DeliveryLineCreate(BaseModel):
    delivery_id: UUID4
    quantity: PositiveInt
    state: Optional[str]
