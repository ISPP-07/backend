from fastapi import HTTPException, status

from src.modules.acat.patient.model import Patient, PatientCreate, PatientOut
from src.core.deps import DataBaseDep
from src.core.database.mongo_types import InsertOneResultMongo
from src.core.utils.helpers import generate_alias


async def get_patients_service(db: DataBaseDep) -> list[Patient]:
    return await Patient.get_multi(db, query=None)


async def create_patient_service(db: DataBaseDep, patient: PatientCreate) -> InsertOneResultMongo:

    # Add alias to the patient
    patient_dict = patient.model_dump()
    patient_dict['alias'] = generate_alias(
        patient_dict['name'],
        patient_dict['first_surname'],
        patient_dict['second_surname']
    )

    result = await Patient.create(db, obj_to_create=patient_dict)
    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    return result


async def get_patient_service(db: DataBaseDep, query: dict) -> PatientOut | None:
    patient = await Patient.get(db, query)

    if not patient:
        return None

    # Add age to the patient
    patient_dict = patient.dict()
    patient_dict['age'] = patient.age()

    return PatientOut(**patient_dict)
