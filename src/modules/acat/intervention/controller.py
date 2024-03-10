from fastapi import HTTPException

from src.modules.acat.intervention.model import Intervention
from src.modules.acat.intervention.service import (
    get_technician_by_id,
    get_patient_by_id,
    create_intervention,
)


async def create_intervention_controller(session, intervention: Intervention):
    technician = await get_technician_by_id(session, intervention.technician_id)
    patient = await get_patient_by_id(session, intervention.patient_id)

    if technician is None or patient is None:
        raise HTTPException(status_code=404, detail="Item not found")

    intervention = await create_intervention(session, intervention)

    return intervention.model_dump()
