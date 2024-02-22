from src.modules.acat.patient.model import Patient


async def get_patient_details_service(session, patient_id: int):
    obj = await Patient.get(session, id=patient_id)
    return obj
