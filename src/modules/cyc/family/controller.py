from src.modules.cyc.family.service import get_families_service


async def get_families_controller(session):
    return await get_families_service(session)
