from uuid import UUID
from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.core.database.mongo_types import InsertOneResultMongo
from src.modules.cyc.product.model import (
    Product,
    Warehouse,
    ProductCreate,
    WarehouseCreate,
    ProductUpdate
)


async def get_products_service(db: DataBaseDep) -> list[Product]:
    return await Product.get_multi(db, query=None)


async def get_warehouses_service(db: DataBaseDep) -> list[Warehouse]:
    return await Warehouse.get_multi(db, query=None)


async def get_product_service(db: DataBaseDep, query: dict) -> Product | None:
    return await Product.get(db, query)


async def get_warehouse_service(db: DataBaseDep, query: dict) -> Warehouse | None:
    return await Warehouse.get(db, query)


async def create_product_service(db: DataBaseDep, product: ProductCreate) -> InsertOneResultMongo:
    result = await Product.create(db, obj_to_create=product.model_dump())
    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    if product.warehouses_id is not None:
        for warehouses_id in product.warehouses_id:
            warehouse = await Warehouse.get(db, {'id': warehouses_id})
            await Warehouse.update(
                db,
                query={'id': warehouses_id},
                data_to_update={
                    'products_id': warehouse.products_id + [result.inserted_id]
                }
            )
    return result


async def create_warehouse_service(
    db: DataBaseDep,
    warehouse: WarehouseCreate
) -> InsertOneResultMongo:
    result = await Warehouse.create(db, obj_to_create=warehouse.model_dump())
    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    if warehouse.products_id is not None:
        for product_id in warehouse.products_id:
            product = await Product.get(db, {'id': product_id})
            await Product.update(
                db,
                query={'id': product_id},
                data_to_update={
                    'warehouses_id': product.warehouses_id + [result.inserted_id]
                }
            )
    return result


async def update_product_service(
    db: DataBaseDep,
    product_id: UUID,
    product_update: ProductUpdate
) -> Product | None:
    return await Product.update(
        db,
        query={'id': product_id},
        data_to_update=product_update.model_dump()
    )


async def delete_product_service(db: DataBaseDep, product_id: UUID) -> None:
    mongo_delete = await Product.delete(db, query={'id': product_id})
    if not mongo_delete.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    warehouses_with_product = await Warehouse.get_multi(
        db,
        query={
            'products_id': {
                '$in': [product_id]
            }
        }
    )
    for warehouse in warehouses_with_product:
        products_id_update = [
            p_id for p_id in warehouse.products_id if p_id != product_id
        ]
        await Warehouse.update(
            db,
            query={'id': warehouse.id},
            data_to_update={'products_id': products_id_update}
        )
