from pydantic import UUID4
from fastapi import HTTPException, status

from src.core.deps import DataBaseDep

from src.modules.acat.intervention import service
from src.modules.acat.intervention.model import InterventionCreate
from src.modules.acat.patient.service import get_patient_by_id


async def get_interventions_controller(db: DataBaseDep):
    return await service.get_interventions_service(db)


async def get_intervention_details_controller(db: DataBaseDep, intervention_id: UUID4):
    result = await service.get_intervention_service(db, query={'id': intervention_id})
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intervention not found",
        )
    return result


async def create_intervention_controller(db: DataBaseDep, intervention: InterventionCreate):

    patient = await get_patient_by_id(db, query={'id': intervention.patient_id})

    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    mongo_insert = await service.create_intervention_service(db, intervention, patient)
    result = await service.get_intervention_service(db, query={'id': mongo_insert.inserted_id})

    return result