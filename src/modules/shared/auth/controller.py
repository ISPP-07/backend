from src.modules.shared.auth import service


def root_controller():
    return service.root_service()


def hello_controller():
    return service.hello_service()
