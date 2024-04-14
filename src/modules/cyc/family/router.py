from typing import Optional

from fastapi import APIRouter, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.server import dependencies
from src.modules.cyc.family import controller
from src.modules.cyc.family import model

router = APIRouter(tags=['Family'], dependencies=dependencies)


@router.get('',
            status_code=status.HTTP_200_OK,
            response_model=model.GetFamilies,
            responses={
                200: {"description": "Successful Response"},
                500: {"description": "Internal Server Error"}
            })
async def get_families(
    db: DataBaseDep,
    state: Optional[model.DerecognitionStatus] = None,
    referred_organization: Optional[str] = None,
    name: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """
    **Retrieve a list of all families.**

    Queries the database and returns a list of all families. Each family includes
    details such as the family ID, name, and related information.
    """
    return await controller.get_families_controller(db, state, referred_organization, name, limit, offset)


@router.post('',
             status_code=status.HTTP_201_CREATED,
             response_model=model.Family,
             responses={
                 201: {"description": "Family created successfully"},
                 400: {"description": "Bad Request - Invalid data input for creating a family"},
                 500: {"description": "Internal Server Error"}
             })
async def create_family(db: DataBaseDep, family: model.FamilyCreate):
    """
    **Create a new family.**

    Accepts family information and creates a new family record in the database. The family
    information includes the family's name and other relevant details.
    """
    return await controller.create_family_controller(db, family)


@router.get('/{family_id}',
            status_code=status.HTTP_200_OK,
            response_model=model.Family,
            responses={
                200: {"description": "Successful Response"},
                404: {"description": "Family not found"},
                500: {"description": "Internal Server Error"}
            })
async def get_family_details(db: DataBaseDep, family_id: UUID4):
    """
    **Get detailed information about a specific family.**

    Fetches and returns detailed information about a specific family identified by its UUID.
    This includes the family's ID, name, and other pertinent details.
    """
    return await controller.get_family_details_controller(db, family_id)


@router.patch('/{family_id}',
              status_code=status.HTTP_200_OK,
              response_model=model.Family,
              responses={
                  200: {"description": "Family updated successfully"},
                  400: {"description": "Bad Request - Invalid data input for updating a family"},
                  404: {"description": "Family not found"},
                  500: {"description": "Internal Server Error"}
              })
async def update_family(db: DataBaseDep, family_id: UUID4, family: model.FamilyUpdate):
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


@router.patch('/{family_id}/person/{person_nid}',
              status_code=status.HTTP_200_OK,
              response_model=model.Family,
              responses={
                  200: {"description": "Person updated successfully"},
                  404: {"description": "Family or person not found"},
                  500: {"description": "Internal Server Error"}
              })
async def update_person(db: DataBaseDep,
                        family_id: UUID4,
                        person_nid: str,
                        person: model.PersonUpdate):
    """
    **Update a person in a family.**

    Accepts information about a person and updates the details of the person in the specified family.
    """
    return await controller.update_person_controller(db, family_id, person_nid, person)


@router.delete('/{family_id}/person/{person_nid}',
               status_code=status.HTTP_204_NO_CONTENT,
               responses={204: {"description": "Person deleted successfully"},
                          404: {"description": "Family or person not found"},
                          400: {"description": "Bad Request - Cannot delete the family head"},
                          500: {"description": "Internal Server Error"}})
async def delete_person(db: DataBaseDep, family_id: UUID4, person_nid: str):
    """
    **Delete a person from a family.**

    Accepts the family and person ID and deletes the person from the specified family.
    """
    await controller.delete_person_controller(db, family_id, person_nid)
    return None
