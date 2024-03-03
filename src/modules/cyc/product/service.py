from src.modules.cyc.product.model import Product, Warehouse


async def get_products_service(session):
    return await Product.get_multi(session)
  

async def create_product_service(session, product: Product):
    return await Product.create(session, **product.model_dump())


async def create_warehouse_service(session, warehouse: Warehouse):
    return await Warehouse.create(session, **warehouse.model_dump())
