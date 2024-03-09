from src.modules.acat.patient.model import Patient


async def create_patient_service(session, patient: Patient):
    obj = await Patient.create(session, **patient.model_dump())
    return obj


async def get_patients_service(session):
    obj = await Patient.get_multi(session, query=None)
    return obj


async def get_patient_details_service(session, patient_id: int):
    obj = await Patient.get(session, id=patient_id, query=None)
    return obj
