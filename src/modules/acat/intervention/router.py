from typing import Any
from fastapi import APIRouter, status
from src.core.deps import DataBaseDep
from src.modules.acat.intervention.controller import create_intervention_controller
from src.modules.acat.intervention.model import Intervention, InterventionCreate


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=Intervention)
async def create_intervention(db: DataBaseDep, intervention: InterventionCreate) -> Any:
    return await create_intervention_controller(db, intervention)
