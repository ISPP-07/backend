from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, UUID4, PositiveInt, FutureDatetime

from src.core.database.base_crud import BaseMongo


class State(Enum):
    NEXT = 'next'
    NOTIFIED = 'notified'
    DELIVERED = 'delivered'


class DeliveryLine(BaseModel):
    product_id: UUID4
    quantity: PositiveInt
    state: Optional[str]


class DeliveryLineOut(DeliveryLine):
    name: Optional[str]


class Delivery(BaseMongo):
    id: UUID4
    date: datetime
    months: PositiveInt
    state: State
    lines: list[DeliveryLine]
    family_id: UUID4


class DeliveryOut(BaseModel):
    id: UUID4
    date: datetime
    months: PositiveInt
    state: State
    lines: list[DeliveryLineOut]
    family_id: UUID4


class DeliveryCreate(BaseModel):
    date: FutureDatetime
    months: PositiveInt
    state: State = State.NEXT
    lines: list[DeliveryLine]
    family_id: UUID4
