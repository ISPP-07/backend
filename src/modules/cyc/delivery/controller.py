from collections import Counter
from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.modules.cyc.delivery.model import Delivery, DeliveryCreate
from src.modules.cyc.delivery import service
from src.modules.cyc.family import service as family_service
from src.modules.cyc.warehouse import service as product_service
from src.modules.cyc.warehouse.model import Product, WarehouseUpdate


async def get_deliveries_controller(db: DataBaseDep):
    return await service.get_deliveries_service(db)


async def get_delivery_details_controller(db: DataBaseDep, delivery_id: int) -> Delivery:
    result = await service.get_delivery_service(db, query={'id': delivery_id})
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Delivery not found',
        )
    return result


async def create_delivery_controller(db: DataBaseDep, create_delivery: DeliveryCreate) -> Delivery:
    # Validate product uniqueness in lines
    products_count = Counter(line.product_id for line in create_delivery.lines)
    if any(count > 1 for count in products_count.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='There is one product that is in two different lines.' +
            'Please put them in a single line'
        )

    # Ensure family exists
    family = await family_service.get_family_service(db, query={'id': create_delivery.family_id})
    if family is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Family {create_delivery.family_id} not found'
        )

    # Fetch warehouses and validate all products exist and have enough stock
    warehouses = await product_service.get_warehouses_service(db, query=None)
    product_to_warehouse = {product.id: (warehouse, product) for warehouse in warehouses
                            for product in warehouse.products}

    missing_products = [product_id for product_id in products_count
                        if product_id not in product_to_warehouse]
    if missing_products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found in any warehouse'
        )

    for product_id, required_quantity in ((line.product_id, line.quantity)
                                          for line in create_delivery.lines):
        warehouse, product = product_to_warehouse.get(product_id, (None, None))
        if not warehouse or product.quantity < required_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Not enough stock for product {product.name}.' +
                f'There is only {product.quantity} left' if warehouse else 'Product not found'
            )

    # Proceed with updating the product quantities in their respective warehouses
    for line in create_delivery.lines:
        warehouse, product = product_to_warehouse[line.product_id]
        updated_products = [p for p in warehouse.products if p.id != line.product_id] + [
            Product(
                id=product.id,
                name=product.name,
                quantity=product.quantity - line.quantity,
                exp_date=product.exp_date
            )
        ]
        await product_service.update_warehouse_service(
            db,
            warehouse_id=warehouse.id,
            warehouse_update=WarehouseUpdate(products=updated_products)
        )

    # Create and retrieve the delivery
    mongo_insert = await service.create_delivery_service(db, create_delivery)
    result = await service.get_delivery_service(db, query={'id': mongo_insert.inserted_id})
    return result
