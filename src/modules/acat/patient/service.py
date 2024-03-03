from src.modules.acat.patient.model import Patient

async def create_patient_service(session, patient: Patient):
    obj = await Patient.create(session, **patient.model_dump())
    return obj

async def get_patients_service(session):
    obj = await Patient.get_multi(session)
    return obj
