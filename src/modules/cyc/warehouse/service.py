from fastapi import HTTPException, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.core.database.mongo_types import InsertOneResultMongo, DeleteResultMongo
from src.modules.cyc.warehouse.model import (
    Warehouse,
    WarehouseUpdate,
    WarehouseCreate,
)


async def get_warehouses_service(db: DataBaseDep, query: dict) -> list[Warehouse]:
    return await Warehouse.get_multi(db, query)


async def get_warehouse_service(db: DataBaseDep, query: dict) -> Warehouse | None:
    return await Warehouse.get(db, query)


async def create_warehouse_service(
    db: DataBaseDep,
    warehouse: WarehouseCreate
) -> InsertOneResultMongo:
    result: InsertOneResultMongo = await Warehouse.create(db, obj_to_create=warehouse.model_dump())
    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    return result


async def update_warehouse_service(
    db: DataBaseDep,
    warehouse_id: UUID4,
    warehouse_update: WarehouseUpdate
) -> Warehouse | None:
    return await Warehouse.update(
        db,
        query={'id': warehouse_id},
        data_to_update=warehouse_update.model_dump()
    )


async def delete_warehouse_service(db: DataBaseDep, warehouse_id: UUID4) -> None:
    mongo_delete: DeleteResultMongo = await Warehouse.delete(db, query={'id': warehouse_id})
    if not mongo_delete.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
