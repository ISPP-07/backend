from src.modules.acat.patient import service
from src.modules.acat.patient.model import Patient


def create_patient_controller(session, patient: Patient):
    return service.create_patient_service(session, patient)


def get_patients_controller(session):
    return service.get_patients_service(session)


def get_patient_details_controller(session, patient_id: int):
    return service.get_patient_details_service(session, patient_id)
