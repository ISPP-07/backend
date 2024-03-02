from src.modules.cyc.product.model import Product


async def get_products_service(session):
    return await Product.get_multi(session)
