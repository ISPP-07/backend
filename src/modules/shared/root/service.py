
from src.modules.shared.root.model import Potato


def root_service():
    return 'Hello from root service!'


async def get_potato_service(session, potato_id):
    obj = await Potato.get(session, id=potato_id)
    return obj


async def create_potato_service(session, potato: Potato):
    obj = await Potato.create(session, **potato.model_dump())
    return obj
