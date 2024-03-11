from fastapi import APIRouter, status
from pydantic import UUID4

from src.core.deps import DataBaseDep

from src.modules.acat.intervention import controller
from src.modules.acat.intervention.model import Intervention, InterventionCreate


router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK,
            response_model=list[Intervention])
async def get_interventions(db: DataBaseDep):
    return await controller.get_interventions_controller(db)


@router.get('/{intervention_id}',
            status_code=status.HTTP_200_OK,
            response_model=Intervention)
async def get_intervention(db: DataBaseDep, intervention_id: UUID4):
    return await controller.get_intervention_details_controller(db, intervention_id)


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=Intervention)
async def create_intervention(db: DataBaseDep, intervention: InterventionCreate):
    return await controller.create_intervention_controller(db, intervention)
