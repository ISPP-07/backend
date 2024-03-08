from fastapi import HTTPException, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.modules.cyc.warehouse import service
from src.modules.cyc.warehouse.model import (
    Product,
    Warehouse,
    ProductCreate,
    ProductUpdate,
    WarehouseCreate,
    WarehouseUpdate,
    ProductOut,
)


async def get_products_controller(db: DataBaseDep) -> list[ProductOut]:
    warehouses = await service.get_warehouses_service(db, query=None)
    result = [
        ProductOut(
            name=product.name,
            quantity=product.quantity,
            exp_date=product.exp_date,
            warehouse_id=warehouse.id,
        )
        for warehouse in warehouses
        for product in warehouse.products
    ]
    return result


async def get_warehouses_controller(db: DataBaseDep) -> list[Warehouse]:
    return await service.get_warehouses_service(db, query=None)


async def create_product_controller(db: DataBaseDep, product: ProductCreate) -> list[ProductOut]:
    result = []
    for item in product.warehouses:
        warehouse = await service.get_warehouse_service(
            db,
            query={'id': item.warehouses_id}
        )
        if warehouse is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Warehouse {item.warehouses_id} not found'
            )
        if any(p.name == product.name for p in warehouse.products):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(f'Product with name {product.name} '
                        f'already exists in warehouse {warehouse.name}')
            )
        await service.update_warehouse_service(
            db,
            warehouse_id=warehouse.id,
            warehouse_update=WarehouseUpdate(
                name=None,
                products=warehouse.products + [Product(
                    name=product.name, quantity=item.quantity, exp_date=product.exp_date
                )]
            )
        )
        result.append(ProductOut(
            warehouse_id=warehouse.id,
            name=product.name,
            quantity=item.quantity,
            exp_date=product.exp_date
        ))
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
    return result


async def update_product_controller(
        db: DataBaseDep,
        product_update: ProductUpdate
) -> list[ProductOut]:
    result = []
    warehouses = await service.get_warehouses_service(
        db,
        query={'id': {'$in': product_update.warehouses_id}}
    )
    for warehouse in warehouses:
        if product_update.name not in (p.name for p in warehouse.products):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Product not found in warehouse {warehouse.name}'
            )
        products = list(filter(
            lambda p: p.name != product_update.name,
            warehouse.products
        )) + [Product(
            name=product_update.name,
            quantity=product_update.quantity,
            exp_date=product_update.exp_date
        )]
        await service.update_warehouse_service(
            db,
            warehouse_id=warehouse.id,
            warehouse_update=WarehouseUpdate(
                name=None,
                products=products
            )
        )
        result.append(ProductOut(
            warehouse_id=warehouse.id,
            name=product_update.name,
            quantity=product_update.quantity,
            exp_date=product_update.exp_date
        ))
    return result


async def delete_warehouse_controller(db: DataBaseDep, warehouse_id: UUID4) -> None:
    await service.delete_warehouse_service(db, warehouse_id)
