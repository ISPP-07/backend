from src.modules.cyc.family.model import Family


async def create_family_service(session, family: Family):
    obj = await Family.create(session, **family.model_dump())
    return obj
