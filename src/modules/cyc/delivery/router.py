from fastapi import APIRouter, status
from src.core.deps import DataBaseDep
from typing import List
from src.modules.cyc.delivery import controller
from src.modules.cyc.delivery.model import Delivery

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Delivery])
async def get_deliveries(db: DataBaseDep) -> List[Delivery]:
    return await controller.get_deliveries_controller(db)

