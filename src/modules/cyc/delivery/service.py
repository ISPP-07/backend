from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.modules.cyc.delivery.model import Delivery, DeliveryCreate
from src.core.database.mongo_types import InsertOneResultMongo


async def get_delivery_service(db: DataBaseDep, query: dict) -> Delivery | None:
    return await Delivery.get(db, query)


async def create_delivery_service(
    db: DataBaseDep,
    delivery: DeliveryCreate,
) -> InsertOneResultMongo:
    result = await Delivery.create(db, obj_to_create=delivery.model_dump())
    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    return result
