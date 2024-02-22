from src.modules.acat.patient import service
from src.modules.acat.patient.model import Patient


def create_patient_controller(session, patient: Patient):
    return service.create_patient_service(session, patient)