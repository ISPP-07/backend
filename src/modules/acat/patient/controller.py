from src.modules.acat.patient.service import get_patient_details_service


def get_patient_details_controller(session, patient_id: int):
    return get_patient_details_service(session, patient_id)
