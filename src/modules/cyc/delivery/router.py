from typing import Optional
from datetime import date

from pydantic import UUID4
from fastapi import APIRouter, status, UploadFile

from src.core.deps import DataBaseDep
from src.server import dependencies
from src.modules.cyc.delivery import controller
from src.modules.cyc.delivery import model

router = APIRouter(tags=["Delivery"], dependencies=dependencies)


@router.get("",
            status_code=status.HTTP_200_OK,
            response_model=model.GetDeliveries,
            responses={
                200: {"description": "Successful Response"},
                500: {"description": "Internal Server Error"}
            })
async def get_deliveries(
    db: DataBaseDep,
    before_date: Optional[date] = None,
    after_date: Optional[date] = None,
    state: Optional[model.State] = None,
    family: Optional[UUID4] = None,
    limit: int = 100,
    offset: int = 0
):
    """
    **Retrieve a list of all deliveries.**

    Queries the database and returns a list containing every delivery, with each delivery detailing
    its ID, date scheduled for, duration in months, items (lines) including product ID, quantity,
    and state (if any), and the family ID associated with the delivery.
    """
    return await controller.get_deliveries_controller(
        db,
        before_date, after_date, state, family,
        limit, offset
    )


@router.get('/{delivery_id}',
            status_code=status.HTTP_200_OK,
            response_model=model.DeliveryOut,
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
             response_model=model.Delivery,
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
async def create_delivery(db: DataBaseDep, delivery: model.DeliveryCreate):
    """
    **Create a new delivery.**

    Accepts delivery information and creates a new delivery record in the database.
    The delivery information includes the scheduled date, duration in months, item lines with
    product ID and quantity,
    and the associated family ID.
    """
    return await controller.create_delivery_controller(db, delivery)


@router.post(
    '/excel',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        200: {"description": "Deliveries in excel created successfully"},
        400: {"description": "The data was incorrect"},
        404: {"description": "Not found"},
    }
)
async def upload_excel_delivery(db: DataBaseDep, deliveries: UploadFile):
    return await controller.upload_excel_deliveries_controller(db, deliveries)


@router.get('/family/{family_id}',
            status_code=status.HTTP_200_OK,
            response_model=list[model.DeliveryOut],
            responses={
                200: {"description": "Successful Response"},
                404: {"description": "There are no deliveries for this family"},
                500: {"description": "Internal Server Error"}
            })
async def get_family_deliveries_details(db: DataBaseDep, family_id: UUID4):
    """
    **Get deliveries information about a specific family.**

    Fetches and returns detailed information about deliveries identified a list.
    Each element includes the delivery's ID, the scheduled date, duration in months, item lines
    with product ID, quantity, state (if specified) and the associated family ID.
    """
    return await controller.get_family_deliveries_controller(db, family_id)


@router.patch('/{delivery_id}',
              status_code=status.HTTP_200_OK,
              response_model=model.Delivery,
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
async def update_delivery(db: DataBaseDep, delivery_id: UUID4, delivery: model.DeliveryUpdate):
    return await controller.update_delivery_controller(db, delivery_id, delivery)


@router.delete('/{delivery_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               responses={
                   204: {"description": "Delivery deleted successfully"},
                   404: {"description": "Delivery not found"},
                   500: {"description": "Internal Server Error"}
               },
               response_model=None)
async def delete_delivery(db: DataBaseDep, delivery_id: UUID4):
    '''
    **Delete delivery by id.**
    '''
    return await controller.delete_delivery_controller(db, delivery_id)
