from src.modules.cyc.product import service
from src.modules.cyc.product.model import Product, Warehouse


async def get_products_controller(session):
    return await service.get_products_service(session)

  
async def create_product_controller(session, product: Product):
    return await service.create_product_service(session, product)

  
async def create_warehouse_controller(session, warehouse: Warehouse):
    return await service.create_warehouse_service(session, warehouse)
