from src.modules.cyc.family.model import Family


async def get_families_service(session):
    return await Family.get_multi(session)
