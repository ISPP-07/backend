from src.modules.cyc.family.model import Family


async def get_families_service(session):
    return await Family.get_multi(session)


async def create_family_service(session, family: Family):
    return await Family.create(session, **family.model_dump())
