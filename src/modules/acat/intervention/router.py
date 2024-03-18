from pydantic import UUID4

from fastapi import APIRouter, status

from src.core.deps import DataBaseDep
from src.modules.acat.intervention import controller
from src.modules.acat.intervention import model


router = APIRouter(tags=['Intervention'])


@router.get('',
            status_code=status.HTTP_200_OK,
            response_model=list[model.Intervention],
            responses={
                200: {"description": "Successful Response"},
                500: {"description": "Internal Server Error"}
            })
async def get_interventions(db: DataBaseDep):
    """
    **Retrieve a list of all interventions.**

    Queries the database and returns a list containing every intervention. Each intervention
    includes its ID, date of the intervention, reason for the intervention (if provided),
    typology (if provided), observations (if provided), the technician responsible for the
    intervention, and the patient associated with the intervention.
    """
    return await controller.get_interventions_controller(db)


@router.get('/{intervention_id}',
            status_code=status.HTTP_200_OK,
            response_model=model.Intervention,
            responses={
                200: {"description": "Successful Response"},
                404: {"description": "Intervention not found"},
                500: {"description": "Internal Server Error"}
            })
async def get_intervention(db: DataBaseDep, intervention_id: UUID4):
    """
    **Get detailed information about a specific intervention.**

    Fetches and returns detailed information about a specific intervention identified by its UUID.
    This includes the intervention's ID, date, reason (if any), typology (if any), observations
    (if any), the technician's name, and detailed patient information.
    """
    return await controller.get_intervention_details_controller(db, intervention_id)


@router.post('',
             status_code=status.HTTP_201_CREATED,
             response_model=model.Intervention,
             responses={
                 201: {"description": "Intervention created successfully"},
                 404: {"description": "Patient not found"},
                 500: {"description": "Internal Server Error"}
             })
async def create_intervention(db: DataBaseDep, intervention: model.InterventionCreate):
    """
    **Create a new intervention.**

    Accepts and processes information to create a new intervention record in the database.
    The required information includes the date of the intervention, the patient's ID, and the
    technician's name. Optional fields are the reason for the intervention, its typology, and
    any observations.
    """
    return await controller.create_intervention_controller(db, intervention)
