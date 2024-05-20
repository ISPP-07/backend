from typing import Any

from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.core.database.base_crud import BulkOperation
from src.core.database.mongo_types import InsertOneResultMongo, BulkWriteResult
from src.core.utils.helpers import get_all_combinations
from src.modules.cyc.delivery import model
from src.modules.cyc.warehouse import service as warehouse_service, model as warehouse_model


async def get_deliveries_service(
    db: DataBaseDep,
    *args: Any,
    **kwargs: Any
) -> list[model.Delivery]:
    query_combinations = get_all_combinations(args)
    query: dict = None
    for combination in query_combinations:
        if any(c[1] is None for c in combination):
            continue
        query = {c[0]: c[1] for c in combination}
        date_queries = [c for c in combination if c[0] == 'date']
        if len(date_queries) == 2:
            query['date'] = dict(
                date_queries[0][1], **date_queries[1][1]
            )
    return await model.Delivery.get_multi(db, query=query, **kwargs)


async def get_delivery_service(db: DataBaseDep, query: dict) -> model.Delivery | None:
    return await model.Delivery.get(db, query)


async def create_delivery_service(
    db: DataBaseDep,
    delivery: model.DeliveryCreate,
) -> InsertOneResultMongo:
    result = await model.Delivery.create(db, obj_to_create=delivery.model_dump())
    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    return result


async def update_delivery_service(
    db: DataBaseDep,
    query: dict,
    delivery: dict,
) -> model.Delivery | None:
    delivery_db: model.Delivery | None = await model.Delivery.update(db, query, delivery)
    if delivery_db is None:
        return None
    result = model.Delivery(id=delivery_db.id,
                            date=delivery_db.date,
                            months=delivery_db.months,
                            state=delivery_db.state,
                            lines=delivery_db.lines,
                            family_id=delivery_db.family_id)
    return result


async def delete_delivery_service(db: DataBaseDep, query: dict) -> None:
    # Recuperar el pedido de entrega
    delivery = await get_delivery_service(db, query)
    if delivery is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Delivery not found'
        )
    if delivery.state != model.State.DELIVERED:
        warehouses = await warehouse_service.get_warehouses_service(db, query=None)
        product_to_warehouse = {
            product.id: (
                warehouse,
                product) for warehouse in warehouses for product in warehouse.products}
        product_updates = {}
        for line in delivery.lines:
            if line.product_id in product_to_warehouse:
                _, product = product_to_warehouse[line.product_id]
                if product.id not in product_updates:
                    product_updates[product.id] = product.quantity + \
                        line.quantity
                else:
                    product_updates[product.id] += line.quantity
        for warehouse in warehouses:
            updated_products = []
            for product in warehouse.products:
                if product.id in product_updates:
                    updated_quantity = product_updates[product.id]
                    updated_product = warehouse_model.Product(
                        id=product.id,
                        name=product.name,
                        quantity=updated_quantity,
                        exp_date=product.exp_date
                    )
                else:
                    updated_product = product
                updated_products.append(updated_product.model_dump())

            await warehouse_service.update_warehouse_service(
                db,
                warehouse_id=warehouse.id,
                warehouse_update={'products': updated_products}
            )

    mongo_delete = await model.Delivery.delete(db, query)
    if not mongo_delete.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error during deletion'
        )


async def count_deliveries_service(db: DataBaseDep, query: dict) -> int:
    return await model.Delivery.count(db, query)


async def bulk_service(db: DataBaseDep, operations: list[BulkOperation], **kwargs: Any):
    result: BulkWriteResult = await model.Delivery.bulk_operation(
        db,
        [o.operation() for o in operations],
        **kwargs
    )
    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    return result
