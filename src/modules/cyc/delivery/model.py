from typing import Optional, Self

from pydantic import BaseModel, UUID4, PositiveInt, FutureDatetime, model_validator
from src.core.deps import DataBaseDep, get_db
from src.core.database.base_crud import BaseMongo
from src.modules.cyc.warehouse.controller import get_products_controller
from src.modules.cyc.warehouse.model import Product
from motor.motor_asyncio import AsyncIOMotorDatabase


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
