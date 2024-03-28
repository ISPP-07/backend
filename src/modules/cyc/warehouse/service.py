from typing import Any
from pydantic import UUID4

from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.core.database.mongo_types import InsertOneResultMongo, DeleteResultMongo, UpdateResult
from src.modules.cyc.warehouse import model


async def get_warehouses_service(db: DataBaseDep, query: dict = None) -> list[model.Warehouse]:
    return await model.Warehouse.get_multi(db, query)


async def get_warehouse_service(db: DataBaseDep, query: dict) -> model.Warehouse | None:
    return await model.Warehouse.get(db, query)


async def get_products_service(db: DataBaseDep, query: dict = None) -> list[model.ProductOut]:
    warehouses: list[model.Warehouse] = await model.Warehouse.get_multi(db, query)
    result = [
        model.ProductOut(
            id=product.id,
            name=product.name,
            quantity=product.quantity,
            exp_date=product.exp_date,
            warehouse_id=warehouse.id,
        )
        for warehouse in warehouses
        for product in warehouse.products
    ]
    return result


async def create_warehouse_service(
    db: DataBaseDep,
    warehouse: dict
) -> InsertOneResultMongo:
    result: InsertOneResultMongo = await model.Warehouse.create(
        db, obj_to_create=warehouse
    )
    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    return result


async def update_warehouse_service(
    db: DataBaseDep,
    warehouse_id: UUID4,
    warehouse_update: dict
) -> model.Warehouse | None:
    return await model.Warehouse.update(
        db,
        query={'id': warehouse_id},
        data_to_update=warehouse_update
    )


async def update_many_warehouse_service(
    db: DataBaseDep,
    query: dict,
    warehouse_update: model.WarehouseProductUpdate,
    **kwargs: Any,
) -> UpdateResult:
    return await model.Warehouse.update_many(
        db,
        query=query,
        data_to_update=warehouse_update,
        **kwargs
    )


async def delete_warehouse_service(db: DataBaseDep, warehouse_id: UUID4) -> None:
    mongo_delete: DeleteResultMongo = await model.Warehouse.delete(db, query={'id': warehouse_id})
    if not mongo_delete.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )


async def get_products_service(db: DataBaseDep) -> list[model.ProductOut]:
    warehouses = await get_warehouses_service(db, query=None)
    result = [
        model.ProductOut(
            id=product.id,
            name=product.name,
            quantity=product.quantity,
            exp_date=product.exp_date,
            warehouse_id=warehouse.id,
        )
        for warehouse in warehouses
        for product in warehouse.products
    ]
    return result
