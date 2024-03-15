from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.modules.cyc.delivery.model import Delivery
from src.modules.cyc.delivery import service


async def get_delivery_details_controller(db: DataBaseDep, delivery_id: int) -> Delivery:
    result = await service.get_delivery_service(db, query={'id': delivery_id})
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Delivery not found',
        )
    return result
