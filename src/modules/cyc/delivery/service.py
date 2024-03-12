from src.core.deps import DataBaseDep
from src.modules.cyc.delivery.model import Delivery


async def get_delivery_service(db: DataBaseDep, query: dict) -> Delivery | None:
    return await Delivery.get(db, query)
