from fastapi import HTTPException, status

from src.modules.acat.patient.model import Patient, PatientCreate
from src.core.deps import DataBaseDep
from src.core.database.mongo_types import InsertOneResultMongo


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


async def get_patient_service(db: DataBaseDep, query: dict) -> Patient | None:
    patient = await Patient.get(db, query)

    # Add age to the patient
    if patient:
        patient_dict = patient.dict()
        patient_dict['age'] = patient.age()

        return patient_dict

    return None


# Auxiliary function to generate the alias
def generate_alias(name: str, first_surname: str, second_surname: str) -> str:
    name_split = name.split()
    number_of_names = len(name_split)
    if number_of_names > 1:
        alias = f"{name_split[0][0]}{name_split[1][0]}{first_surname[:2]}{second_surname[:2]}"
    else:
        alias = f"{name[:2]}{first_surname[:2]}{second_surname[:2]}"
    return alias.lower()
