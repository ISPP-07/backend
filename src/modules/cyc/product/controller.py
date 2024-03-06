from uuid import UUID
from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.modules.cyc.product import service
from src.modules.cyc.product.model import (
    Product,
    Warehouse,
    ProductCreate,
    WarehouseCreate,
    ProductUpdate
)


async def get_products_controller(db: DataBaseDep) -> list[Product]:
    return await service.get_products_service(db)


async def get_warehouses_controller(db: DataBaseDep) -> list[Warehouse]:
    return await service.get_warehouses_service(db)


async def create_product_controller(db: DataBaseDep, product: ProductCreate) -> Product:
    mongo_insert = await service.create_product_service(db, product)
    result = await service.get_product_service(db, query={'id': mongo_insert.inserted_id})
    return result


async def create_warehouse_controller(db: DataBaseDep, warehouse: WarehouseCreate) -> Warehouse:
    check_warehouse = await service.get_warehouse_service(db, query={'name': warehouse.name})
    if check_warehouse is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Warehouse already created'
        )
    mongo_insert = await service.create_warehouse_service(db, warehouse)
    result = await service.get_warehouse_service(db, query={'id': mongo_insert.inserted_id})
    print('Warehouse: ', result)
    return result


async def update_product_controller(
        db: DataBaseDep,
        product_id: UUID,
        product_update: ProductUpdate
) -> Product:
    result = await service.update_product_service(db, product_id, product_update)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )
    return result


async def delete_product_controller(db: DataBaseDep, product_id: UUID) -> None:
    await service.delete_product_service(db, product_id)
