from src.modules.acat.patient import service

def get_patients_controller(session):
    return service.get_patients_service(session)
