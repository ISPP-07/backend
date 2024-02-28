from src.modules.cyc.family.model import Family
from src.modules.cyc.family import service


async def create_family_controller(session, family: Family):
    return await service.create_family_service(session, family)

def get_family_details_controller(session, family_id: int):
    return service.get_family_details_service(session, family_id)