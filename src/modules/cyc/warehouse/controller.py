from pydantic import UUID4
from uuid import uuid4
from collections import Counter

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
    warehouses_id = [p.warehouse_id for p in create_products.products]
    warehouses = await service.get_warehouses_service(db, query={'id': {'$in': warehouses_id}})
    products_by_warehouse: dict[UUID4, list[dict]] = {}
    products_count = Counter([p.name for p in create_products.products])
    if any(count > 1 for count in products_count.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='There can not be duplicated products'
        )
    for product in create_products.products:
        warehouse = next(
            (w for w in warehouses if w.id if product.warehouse_id),
            None
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
            id=uuid4(),
            name=product.name,
            quantity=product.quantity,
            exp_date=product.exp_date
        ).model_dump()
        if warehouse.id not in products_by_warehouse:
            products_by_warehouse[warehouse.id] = []
        products_by_warehouse[warehouse.id].append(new_product)
        result.append(model.ProductOut(
            id=new_product['id'],
            warehouse_id=warehouse.id,
            name=product.name,
            quantity=product.quantity,
            exp_date=product.exp_date
        ))
    for key, value in products_by_warehouse.items():
        warehouse = [w for w in warehouses if w.id == key][0]
        warehouse_products = [
            p.model_dump() for p
            in warehouse.products
        ]
        await service.update_warehouse_service(
            db,
            warehouse_id=warehouse.id,
            warehouse_update={'products': warehouse_products + value}
        )
    return result


async def create_warehouse_controller(
    db: DataBaseDep,
    warehouse: model.WarehouseCreate
) -> model.Warehouse:
    check_warehouse = await service.get_warehouse_service(db, query={'name': warehouse.name})
    if check_warehouse is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Warehouse already created'
        )
    new_warehouse = warehouse.model_dump()
    products_with_id = [
        model.Product(
            id=uuid4(),
            name=p.name,
            quantity=p.quantity,
            exp_date=p.exp_date
        ) for p in warehouse.products
    ]
    new_warehouse['products'] = products_with_id
    mongo_insert = await service.create_warehouse_service(db, new_warehouse)
    result = await service.get_warehouse_service(db, query={'id': mongo_insert.inserted_id})
    return result


async def update_product_controller(
        db: DataBaseDep,
        update_products: model.ProductUpdate
) -> list[model.ProductOut]:
    result = []
    warehouses_id = [p.warehouse_id for p in update_products.products]
    warehouses = await service.get_warehouses_service(db, query={'id': {'$in': warehouses_id}})
    products_by_warehouse: dict[UUID4, list[model.Product]] = {}
    product_ids_count = Counter(p.product_id for p in update_products.products)
    if any(value > 1 for value in product_ids_count.values):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There cannot be duplicated products'
        )
    for product in update_products.products:
        warehouse = next(
            (w for w in warehouses if w.id if product.warehouse_id),
            None
        )
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
            lambda p: p.id == product.product_id,
            warehouse.products
        )).pop()
        warehouse.products.remove(old_product)
        updated_product = model.Product(
            id=product.product_id,
            name=old_product.name if product.name is None else product.name,
            quantity=old_product.quantity if product.quantity is None else product. quantity,
            exp_date=product.exp_date if product.update_exp_date else old_product.exp_date)
        if warehouse.id not in products_by_warehouse:
            products_by_warehouse[warehouse.id] = []
        products_by_warehouse[warehouse.id].append(updated_product)
        result.append(model.ProductOut(
            id=product.product_id,
            warehouse_id=warehouse.id,
            name=updated_product.name,
            quantity=updated_product.quantity,
            exp_date=updated_product.exp_date
        ))
    for key, value in products_by_warehouse.items():
        warehouse = [w for w in warehouses if w.id == key][0]
        await service.update_warehouse_service(
            db,
            warehouse_id=warehouse.id,
            warehouse_update=model.WarehouseUpdate(
                products=warehouse.products + value
            )
        )
    return result


async def delete_warehouse_controller(db: DataBaseDep, warehouse_id: UUID4) -> None:
    await service.delete_warehouse_service(db, warehouse_id)
