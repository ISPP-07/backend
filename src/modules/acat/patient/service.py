from src.modules.acat.patient.model import Patient

async def get_patients_service(session):
    obj = await Patient.get_multi(session)
    return obj
