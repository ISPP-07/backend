from typing import Optional
from pydantic import BaseModel, UUID4, PositiveInt, FutureDatetime

from src.core.database.base_crud import BaseMongo


class DeliveryLine(BaseModel):
    product_id: UUID4
    quantity: PositiveInt
    state: Optional[str]


class Delivery(BaseMongo):
    id: UUID4
    date: FutureDatetime
    months: PositiveInt
    lines: list[DeliveryLine]
    family_id: UUID4


class DeliveryCreate(BaseModel):
    date: FutureDatetime
    months: PositiveInt
    lines: list[DeliveryLine]
    family_id: UUID4
