from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.core.database.mongo_types import InsertOneResultMongo
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
