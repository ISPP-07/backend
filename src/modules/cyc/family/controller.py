from src.modules.cyc.family.model import Family
from src.modules.cyc.family import service


async def create_family_controller(session, family: Family):
    return await service.create_family_service(session, family)
