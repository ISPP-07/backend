from src.modules.cyc.product import service


async def get_products_controller(session):
    return await service.get_products_service(session)
