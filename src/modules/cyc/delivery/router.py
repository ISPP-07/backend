from typing import List
from pydantic import UUID4

from fastapi import APIRouter, status

from src.core.deps import DataBaseDep
from src.modules.cyc.delivery import controller
from src.modules.cyc.delivery.model import Delivery, DeliveryCreate

router = APIRouter(tags=["Delivery"])


@router.get("",
            status_code=status.HTTP_200_OK,
            response_model=List[Delivery],
            responses={
                200: {"description": "Successful Response"},
                500: {"description": "Internal Server Error"}
            })
async def get_deliveries(db: DataBaseDep) -> List[Delivery]:
    """
    **Retrieve a list of all deliveries.**

    Queries the database and returns a list containing every delivery, with each delivery detailing
    its ID, date scheduled for, duration in months, items (lines) including product ID, quantity,
    and state (if any), and the family ID associated with the delivery.
    """
    return await controller.get_deliveries_controller(db)


@router.get('/{delivery_id}',
            status_code=status.HTTP_200_OK,
            response_model=Delivery,
            responses={
                200: {"description": "Successful Response"},
                404: {"description": "Delivery not found"},
                500: {"description": "Internal Server Error"}
            })
async def get_delivery_details(db: DataBaseDep, delivery_id: UUID4):
    """
    **Get detailed information about a specific delivery.**

    Fetches and returns detailed information about a specific delivery identified by its UUID.
    The information includes the delivery's ID, the scheduled date, duration in months, item lines 
    with product ID, quantity,
    and state (if specified), and the associated family ID.
    """
    return await controller.get_delivery_details_controller(db, delivery_id)


@router.post('',
             status_code=status.HTTP_201_CREATED,
             response_model=Delivery,
             responses={
                 201: {"description": "Delivery created successfully"},
                 400: {
                     "description": "Bad Request - Invalid data input, such as duplicate " +
                     "products in lines, or product stock issues"
                 },
                 404: {
                     "description": "Family not found or Product not found in any warehouse"
                 },
                 500: {"description": "Internal Server Error"}
             })
async def create_delivery(db: DataBaseDep, delivery: DeliveryCreate):
    """
    **Create a new delivery.**

    Accepts delivery information and creates a new delivery record in the database.
    The delivery information includes the scheduled date, duration in months, item lines with 
    product ID and quantity,
    and the associated family ID.
    """
    return await controller.create_delivery_controller(db, delivery)
