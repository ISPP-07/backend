from src.modules.acat.intervention.model import Intervention, Technician
from src.modules.acat.patient.model import Patient


async def get_technician_by_id(session, technician_id: int):
    return await Technician.get(session, id=technician_id, query=None)


async def get_patient_by_id(session, patient_id: int):
    return await Patient.get(session, id=patient_id, query=None)


async def create_intervention(session, intervention_data):
    intervention = await Intervention.create(session, **intervention_data.model_dump())
    return intervention
