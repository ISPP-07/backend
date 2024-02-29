from src.modules.cyc.family.model import Family
from src.modules.cyc.family import service


async def get_families_controller(session):
    return await service.get_families_service(session)


async def create_family_controller(session, family: Family):
    return await service.create_family_service(session, family)
