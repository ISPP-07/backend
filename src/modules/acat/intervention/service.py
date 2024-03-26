from fastapi import HTTPException, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.core.database.mongo_types import DeleteResultMongo, InsertOneResultMongo
from src.modules.acat.intervention import model
from src.modules.acat.patient import model as patient_model


async def get_intervention_service(db: DataBaseDep, query: dict) -> model.Intervention | None:
    intervention = await model.Intervention.get(db, query)

    if not intervention:
        return None

    return intervention


async def get_interventions_service(db: DataBaseDep) -> list[model.Intervention]:
    return await model.Intervention.get_multi(db, query=None)


async def create_intervention_service(db: DataBaseDep, intervention_data: model.InterventionCreate,
                                      patient_data: patient_model.Patient) -> InsertOneResultMongo:
    intervention_dict = intervention_data.model_dump()
    intervention_dict['patient'] = patient_data.model_dump()
    intervention_dict.pop('patient_id')

    result = await model.Intervention.create(db, obj_to_create=intervention_dict)

    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    return result


async def update_intervention_service(
    db: DataBaseDep,
    intervention_id: UUID4,
    updated_intervention_data: dict,
) -> model.Intervention | None:
    return await model.Intervention.update(
        db,
        query={'id': intervention_id},
        data_to_update=updated_intervention_data
    )


async def delete_intervention_service(db: DataBaseDep, query: dict) -> model.Intervention:
    mongo_delete: DeleteResultMongo = await model.Intervention.delete(db, query)

    if mongo_delete.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Intervention not found',
        )

    if not mongo_delete.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
