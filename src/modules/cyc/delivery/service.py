# Delivery service
from src.modules.cyc.delivery.model import Delivery
from src.core.deps import DataBaseDep


async def get_deliveries_service(db: DataBaseDep) -> list[Delivery]:
    return await Delivery.get_multi(db, query=None)


async def get_delivery_service(db: DataBaseDep, query: dict) -> Delivery | None:
    return await Delivery.get(db, query)
