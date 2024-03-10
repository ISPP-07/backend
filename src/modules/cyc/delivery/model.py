from typing import Optional
from pydantic import BaseModel, UUID4, PositiveInt, FutureDatetime
from src.core.database.base_crud import BaseMongo
from src.modules.cyc.warehouse.model import Product


class Delivery(BaseMongo):
    id: UUID4
    date: FutureDatetime
    months: PositiveInt
    products: list[Product]
    family_id: UUID4


class DeliveryCreate(BaseModel):
    date: FutureDatetime
    months: PositiveInt
    products: list[Product]


class DeliveryLineCreate(BaseModel):
    delivery_id: UUID4
    product_id: UUID4
    quantity: PositiveInt
    state: Optional[str]
