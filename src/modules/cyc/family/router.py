from typing import List
from pydantic import UUID4

from fastapi import APIRouter, status, UploadFile

from src.core.deps import DataBaseDep
from src.modules.cyc.family import controller
from src.modules.cyc.family.model import Family, FamilyCreate, FamilyUpdate

router = APIRouter(tags=['Family'])


@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=List[Family],
    responses={
        200: {"description": "Successful Response"},
        500: {"description": "Internal Server Error"}
    }
)
async def get_families(db: DataBaseDep):
    """
    **Retrieve a list of all families.**

    Queries the database and returns a list of all families. Each family includes
    details such as the family ID, name, and related information.
    """
    return await controller.get_families_controller(db)


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=Family,
    responses={
        201: {"description": "Family created successfully"},
        400: {"description": "Bad Request - Invalid data input for creating a family"},
        500: {"description": "Internal Server Error"}
    }
)
async def create_family(db: DataBaseDep, family: FamilyCreate):
    """
    **Create a new family.**

    Accepts family information and creates a new family record in the database. The family
    information includes the family's name and other relevant details.
    """
    return await controller.create_family_controller(db, family)


@router.get(
    '/{family_id}',
    status_code=status.HTTP_200_OK,
    response_model=Family,
    responses={
        200: {"description": "Successful Response"},
        404: {"description": "Family not found"},
        500: {"description": "Internal Server Error"}
    }
)
async def get_family_details(db: DataBaseDep, family_id: UUID4):
    """
    **Get detailed information about a specific family.**

    Fetches and returns detailed information about a specific family identified by its UUID.
    This includes the family's ID, name, and other pertinent details.
    """
    return await controller.get_family_details_controller(db, family_id)


@router.patch('/{family_id}',
              status_code=status.HTTP_200_OK,
              response_model=Family,
              responses={
                  200: {"description": "Family updated successfully"},
                  400: {"description": "Bad Request - Invalid data input for updating a family"},
                  404: {"description": "Family not found"},
                  500: {"description": "Internal Server Error"}
              })
async def update_family(db: DataBaseDep, family_id: UUID4, family: FamilyUpdate):
    """
    **Update an existing family.**

    Accepts updated family information and updates the corresponding family record in the database.
    The family information includes the family's name and other relevant details.
    """
    return await controller.update_family_controller(db, family_id, family)


@router.delete('/{family_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               responses={
                   204: {"description": "Family deleted successfully"},
                   404: {"description": "Family not found"},
                   500: {"description": "Internal Server Error"}
               })
async def delete_family(db: DataBaseDep, family_id: UUID4):
    """
    **Delete a family.**

    Deletes a family record from the database based on the family's UUID.
    """
    return await controller.delete_family_controller(db, family_id)
