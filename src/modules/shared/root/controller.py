from src.modules.shared.root import service
from src.modules.shared.root.model import Potato


def root_controller():
    return service.root_service()


def get_potato_controller(session, potato_id):
    return service.get_potato_service(session, potato_id)


def create_potato_controller(session, potato: Potato):
    return service.create_potato_service(session, potato)
