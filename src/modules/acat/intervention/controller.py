from pydantic import UUID4

from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.modules.acat.intervention import service
from src.modules.acat.intervention import model
from src.modules.acat.patient import service as patient_service


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


async def create_intervention_controller(db: DataBaseDep, intervention: model.InterventionCreate):

    patient = await patient_service.get_patient_service(db, query={'id': intervention.patient_id})

    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    mongo_insert = await service.create_intervention_service(db, intervention, patient)
    result = await service.get_intervention_service(db, query={'id': mongo_insert.inserted_id})

    return result


async def update_intervention_controller(
    db: DataBaseDep,
    intervention_id: UUID4,
    intervention: model.InterventionUpdate
) -> model.Intervention:
    intervention_db = await service.get_intervention_service(db, query={'id': intervention_id})
    if intervention_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Intervention not found',
        )
    request_none_fields = [
        field for field in model.INTERVENTION_NONE_FIELDS
        if field in intervention.update_fields_to_none
    ]

    update_data = intervention.model_dump(exclude={'update_fields_to_none'})

    for field in request_none_fields:
        update_data[field] = None

    for field in list(update_data):
        if update_data[field] is None and field not in request_none_fields:
            del update_data[field]

    updated_intervention = await service.update_intervention_service(
        db,
        intervention_id,
        update_data
    )

    return updated_intervention


async def delete_intervention_controller(db: DataBaseDep, intervention_id: UUID4):
    await service.delete_intervention_service(db, query={'id': intervention_id})
