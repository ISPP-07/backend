from fastapi import APIRouter, status
from typing import List
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.modules.cyc.delivery import controller
from src.modules.cyc.delivery.model import Delivery, DeliveryCreate

router = APIRouter(tags=["Delivery"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Delivery])
async def get_deliveries(db: DataBaseDep) -> List[Delivery]:
    return await controller.get_deliveries_controller(db)


@router.get('/{delivery_id}',
            status_code=status.HTTP_200_OK,
            response_model=Delivery)
async def get_delivery_details(db: DataBaseDep, delivery_id: UUID4):
    return await controller.get_delivery_details_controller(db, delivery_id)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Delivery)
async def create_delivery(db: DataBaseDep, delivery: DeliveryCreate):
    return await controller.create_delivery_controller(db, delivery)
