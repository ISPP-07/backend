from pydantic import UUID4

from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.modules.cyc.warehouse import service
from src.modules.cyc.warehouse import model


async def get_products_controller(db: DataBaseDep) -> list[model.ProductOut]:
    warehouses = await service.get_warehouses_service(db, query=None)
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


async def get_warehouses_controller(db: DataBaseDep) -> list[model.Warehouse]:
    return await service.get_warehouses_service(db, query=None)


async def create_product_controller(
    db: DataBaseDep,
    create_products: model.ProductCreate
) -> list[model.ProductOut]:
    result = []
    for product in create_products.products:
        warehouse = await service.get_warehouse_service(
            db,
            query={'id': product.warehouse_id}
        )
        if warehouse is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Warehouse {product.warehouse_id} not found'
            )
        if any(p.name == product.name for p in warehouse.products):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(f'Product with name {product.name} '
                        f'already exists in warehouse {warehouse.name}')
            )
        new_product = model.Product(
            name=product.name,
            quantity=product.quantity,
            exp_date=product.exp_date
        ).model_dump()
        new_products = [
            p.model_dump() for p
            in warehouse.products
        ]
        await service.update_warehouse_service(
            db,
            warehouse_id=warehouse.id,
            warehouse_update={
                'products': new_products + [new_product]
            }
        )
        result.append(model.ProductOut(
            id=new_product['id'],
            warehouse_id=warehouse.id,
            name=product.name,
            quantity=product.quantity,
            exp_date=product.exp_date
        ))
    return result


async def create_warehouse_controller(db: DataBaseDep,
                                      warehouse: model.WarehouseCreate) -> model.Warehouse:
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
        update_products: model.ProductUpdate
) -> list[model.ProductOut]:
    result = []
    for product in update_products.products:
        warehouse = await service.get_warehouse_service(db, {'id': product.warehouse_id})
        if warehouse is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Warehouse {product.warehouse_id} not found'
            )
        if product.product_id not in (p.id for p in warehouse.products):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Product not found in warehouse {warehouse.name}'
            )
        old_product = list(filter(
            lambda p: p.id == product.product_id,  # pylint: disable="W0640"
            warehouse.products
        )).pop()
        updated_product = model.Product(
            id=product.product_id,
            name=old_product.name if product.name is None else product.name,
            quantity=old_product.quantity if product.quantity is None else product. quantity,
            exp_date=product.exp_date if product.update_exp_date else old_product.exp_date)
        warehouse.products.remove(old_product)
        new_products = warehouse.products + [updated_product]
        await service.update_warehouse_service(
            db,
            warehouse_id=warehouse.id,
            warehouse_update=model.WarehouseUpdate(
                products=new_products
            )
        )
        result.append(model.ProductOut(
            id=product.product_id,
            warehouse_id=warehouse.id,
            name=updated_product.name,
            quantity=updated_product.quantity,
            exp_date=updated_product.exp_date
        ))
    return result


async def delete_warehouse_controller(db: DataBaseDep, warehouse_id: UUID4) -> None:
    await service.delete_warehouse_service(db, warehouse_id)
