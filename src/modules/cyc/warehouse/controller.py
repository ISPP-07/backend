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


async def get_warehouses_controller(db: DataBaseDep) -> list[Warehouse]:
    return await service.get_warehouses_service(db, query=None)


async def create_product_controller(db: DataBaseDep, product: ProductCreate) -> list[ProductOut]:
    result = []
    for item in product.warehouses:
        warehouse = await service.get_warehouse_service(
            db,
            query={'id': item.warehouse_id}
        )
        if warehouse is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Warehouse {item.warehouse_id} not found'
            )
        if any(p.name == product.name for p in warehouse.products):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(f'Product with name {product.name} '
                        f'already exists in warehouse {warehouse.name}')
            )
        new_product = Product(
            name=product.name,
            quantity=item.quantity,
            exp_date=product.exp_date
        )
        await service.update_warehouse_service(
            db,
            warehouse_id=warehouse.id,
            warehouse_update=WarehouseUpdate(
                products=warehouse.products + [new_product]
            )
        )
        result.append(ProductOut(
            id=new_product.id,
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
    for item in product_update.warehouses:
        warehouse = await service.get_warehouse_service(db, {'id': item.warehouse_id})
        if warehouse is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Warehouse {item.warehouse_id} not found'
            )
        if item.product_id not in (p.id for p in warehouse.products):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Product not found in warehouse {warehouse.name}'
            )
        new_products = list(filter(
            lambda p: p.id != item.product_id,  # pylint: disable="W0640"
            warehouse.products
        )) + [Product(
            name=product_update.name,
            quantity=item.quantity,
            exp_date=product_update.exp_date
        )]
        await service.update_warehouse_service(
            db,
            warehouse_id=warehouse.id,
            warehouse_update=WarehouseUpdate(
                products=new_products
            )
        )
        result.append(ProductOut(
            id=item.product_id,
            warehouse_id=warehouse.id,
            name=product_update.name,
            quantity=item.quantity,
            exp_date=product_update.exp_date
        ))
    return result


async def delete_warehouse_controller(db: DataBaseDep, warehouse_id: UUID4) -> None:
    await service.delete_warehouse_service(db, warehouse_id)
