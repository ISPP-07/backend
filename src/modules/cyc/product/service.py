from src.modules.cyc.product.model import Product, Warehouse

async def create_product_service(session, product: Product):
    obj = await Product.create(session, **product.model_dump())
    return product

async def create_warehouse_service(session, warehouse: Warehouse):
    obj = await Warehouse.create(session, **warehouse.model_dump())
    return warehouse
