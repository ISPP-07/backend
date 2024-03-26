from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.modules.cyc.delivery import model
from src.core.database.mongo_types import DeleteResultMongo, InsertOneResultMongo
from src.modules.cyc.warehouse import service as warehouse_service
from src.modules.cyc.warehouse import model as warehouse_model


async def get_deliveries_service(db: DataBaseDep) -> list[model.Delivery]:
    return await model.Delivery.get_multi(db, query=None)


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


async def delete_delivery_service(db: DataBaseDep, query: dict) -> model.Delivery:
    # Reset the stock of the products in the delivery
    delivery = await get_delivery_service(db, query)
    warehouses = await warehouse_service.get_warehouses_service(db, query=None)
    product_to_warehouse = {
        product.id: (
            warehouse,
            product) for warehouse in warehouses for product in warehouse.products}
    if delivery.state != model.State.DELIVERED:
        for line in delivery.lines:
            warehouse, product = product_to_warehouse[line.product_id]
            updated_products = [
                p for p in warehouse.products if p.id != line.product_id] + [
                warehouse_model.Product(
                    id=product.id,
                    name=product.name,
                    quantity=product.quantity + line.quantity,
                    exp_date=product.exp_date)]
            await warehouse_service.update_warehouse_service(
                db,
                warehouse_id=warehouse.id,
                warehouse_update=warehouse_model.WarehouseUpdate(
                    products=updated_products)
            )

    mongo_delete: DeleteResultMongo = await model.Delivery.delete(db, query)
    if mongo_delete.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Delivery not found'
        )
    if not mongo_delete.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
