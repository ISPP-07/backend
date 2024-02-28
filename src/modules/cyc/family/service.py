from src.modules.cyc.family.model import Family


async def create_family_service(session, family: Family):
    obj = await Family.create(session, **family.model_dump())
    return obj

async def get_family_details_service(session, family_id: int):
    obj = await Family.get(session, id=family_id)
    return obj