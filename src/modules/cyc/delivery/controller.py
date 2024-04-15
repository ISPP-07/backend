from collections import Counter
from typing import Dict, Optional
from datetime import date

from pydantic import UUID4
from fastapi import HTTPException, status

from src.core.deps import DataBaseDep
from src.modules.cyc.delivery import model
from src.modules.cyc.delivery import service
from src.modules.cyc.family import service as family_service
from src.modules.cyc.warehouse import service as product_service
from src.modules.cyc.warehouse import model as product_model


async def get_deliveries_controller(
    db: DataBaseDep,
    before_date: Optional[date],
    after_date: Optional[date],
    state: Optional[model.State],
    family: Optional[UUID4],
    limit: int = 100,
    offset: int = 0
) -> model.GetDeliveries:
    deliveries = await service.get_deliveries_service(
        db,
        (
            'date', {
                '$lte': before_date.isoformat()
            } if before_date is not None else None
        ),
        (
            'date', {
                '$gte': after_date.isoformat()
            } if after_date is not None else None
        ),
        (
            'state', state.value if state is not None else state
        ),
        (
            'family_id', family
        ),
        limit=limit,
        skip=offset
    )
    warehouses = await product_service.get_warehouses_service(db, query=None)
    product_to_name = {
        product.id: product.name for warehouse in warehouses for product in warehouse.products
    }
    deliveries_out = []
    for delivery in deliveries:
        updated_lines = []
        for line in delivery.lines:
            product_name = product_to_name.get(line.product_id)
            updated_line = model.DeliveryLineOut(
                **line.model_dump(), name=product_name
            )
            updated_lines.append(updated_line)
        out = model.DeliveryOut(
            id=delivery.id,
            date=delivery.date,
            months=delivery.months,
            state=delivery.state,
            lines=updated_lines,
            family_id=delivery.family_id
        )
        deliveries_out.append(out)
    return model.GetDeliveries(
        elements=deliveries_out,
        total_elements=await service.count_deliveries_service(db, query={})
    )


async def get_delivery_details_controller(db: DataBaseDep, delivery_id: int) -> model.DeliveryOut:
    result = await service.get_delivery_service(db, query={'id': delivery_id})
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Delivery not found',
        )
    warehouses = await product_service.get_warehouses_service(db, query=None)
    product_to_name = {
        product.id: product.name for warehouse in warehouses for product in warehouse.products}

    updated_lines = []
    for line in result.lines:
        product_name = product_to_name.get(line.product_id)
        updated_line = model.DeliveryLineOut(
            **line.model_dump(), name=product_name)
        updated_lines.append(updated_line)
    salida = model.DeliveryOut(id=result.id,
                               date=result.date,
                               months=result.months,
                               state=result.state,
                               lines=updated_lines,
                               family_id=result.family_id)
    return salida


async def create_delivery_controller(db: DataBaseDep, create_delivery: model.DeliveryCreate) -> model.Delivery:
    # Validar la unicidad del producto en las líneas
    products_count = Counter(line.product_id for line in create_delivery.lines)
    if any(count > 1 for count in products_count.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='There is one product that is in two different lines. ' +
            'Please put them in a single line'
        )

    # Asegurar que la familia existe
    family = await family_service.get_family_service(db, query={'id': create_delivery.family_id})
    if family is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Family {create_delivery.family_id} not found'
        )

    # Recuperar almacenes y validar que todos los productos existan y tengan
    # suficiente stock
    warehouses = await product_service.get_warehouses_service(db, query=None)
    product_to_warehouse: Dict[str, tuple] = {product.id: (
        warehouse, product) for warehouse in warehouses for product in warehouse.products}

    missing_products = [
        product_id for product_id in products_count if product_id not in product_to_warehouse]
    if missing_products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found in any warehouse'
        )

    for product_id, required_quantity in (
            (line.product_id, line.quantity) for line in create_delivery.lines):
        warehouse, product = product_to_warehouse.get(product_id, (None, None))
        if not warehouse or product.quantity < required_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Not enough stock for product {product.name}. ' +
                f'There is only {product.quantity} left' if warehouse else 'Product not found')

    # Preparar las actualizaciones por producto
    product_updates = {}  # Diccionario para acumular actualizaciones
    for line in create_delivery.lines:
        warehouse, product = product_to_warehouse[line.product_id]
        if product.id not in product_updates:
            product_updates[product.id] = product.quantity - line.quantity
        else:
            product_updates[product.id] -= line.quantity
    for warehouse in warehouses:
        updated_products = []
        for product in warehouse.products:
            if product.id in product_updates:
                updated_product = product_model.Product(
                    id=product.id,
                    name=product.name,
                    quantity=product_updates[product.id],
                    exp_date=product.exp_date
                )
            else:
                updated_product = product
            updated_products.append(updated_product.model_dump())

        await product_service.update_warehouse_service(
            db,
            warehouse_id=warehouse.id,
            warehouse_update={'products': updated_products}
        )
    mongo_insert = await service.create_delivery_service(db, create_delivery)
    result = await service.get_delivery_service(db, query={'id': mongo_insert.inserted_id})
    return result


async def update_delivery_controller(db: DataBaseDep, delivery_id: UUID4, delivery: model.DeliveryUpdate) -> model.Delivery:
    delivery_actual = await service.get_delivery_service(db, query={'id': delivery_id})
    if delivery_actual is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Delivery not found'
        )

    if delivery_actual.state == model.State.DELIVERED and delivery.state is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot update a delivered delivery'
        )

    # Validar la unicidad del producto en las líneas
    if delivery.lines:
        products_count = Counter(line.product_id for line in delivery.lines)
        if any(count > 1 for count in products_count.values()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='There is one product that is in two different lines. ' +
                'Please put them in a single line')

        warehouses = await product_service.get_warehouses_service(db, query=None)
        product_to_warehouse = {
            product.id: (
                warehouse,
                product) for warehouse in warehouses for product in warehouse.products}

        missing_products = [
            product_id for product_id in products_count if product_id not in product_to_warehouse]
        if missing_products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Product not found in any warehouse'
            )

        product_updates = {}  # Diccionario para acumular diferencias de cantidad
        for line in delivery.lines:
            warehouse, product = product_to_warehouse.get(
                line.product_id, (None, None))
            if not warehouse or product is None:
                continue  # Omitir si el producto no se encuentra en ningún almacén

            # Calcula la diferencia de cantidad basada en la entrega actual y la
            # nueva
            old_quantity = next(
                (old_line.quantity for old_line in delivery_actual.lines if old_line.product_id == line.product_id),
                0)
            quantity_difference = old_quantity - line.quantity

            if product.id not in product_updates:
                product_updates[product.id] = product.quantity + \
                    quantity_difference
            else:
                product_updates[product.id] += quantity_difference

            if product_updates[product.id] < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Not enough stock for product {product.name}.' +
                    f' There is only {product.quantity} left')

        # Proceder con la actualización de las cantidades de los productos en sus
        # respectivos almacenes
        for warehouse in warehouses:
            updated_products = []
            for product in warehouse.products:
                if product.id in product_updates:
                    updated_product = product_model.Product(
                        id=product.id,
                        name=product.name,
                        quantity=product_updates[product.id],
                        exp_date=product.exp_date
                    )
                else:
                    updated_product = product
                updated_products.append(updated_product.model_dump())

            await product_service.update_warehouse_service(
                db,
                warehouse_id=warehouse.id,
                warehouse_update={'products': updated_products}
            )

    # Asegurar que la familia existe
    if delivery.family_id:
        family = await family_service.get_family_service(db, query={'id': delivery.family_id})
        if family is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Family {delivery.family_id} not found'
            )

    update_data = delivery.model_dump()
    for field in update_data.copy():
        if update_data[field] is None:
            update_data.pop(field)
    result = await service.update_delivery_service(db, query={'id': delivery_id}, delivery=update_data)
    return result


async def delete_delivery_controller(db: DataBaseDep, delivery_id: UUID4):
    return await service.delete_delivery_service(db, query={'id': delivery_id})


async def get_family_deliveries_controller(db: DataBaseDep, family_id: int) -> list[model.DeliveryOut]:
    deliveries = await service.get_deliveries_service(db)
    result = [
        delivery for delivery in deliveries if delivery.family_id == family_id]
    warehouses = await product_service.get_warehouses_service(db, query=None)
    product_to_name = {
        product.id: product.name for warehouse in warehouses for product in warehouse.products}
    result_final = []
    for delivery in result:
        updated_lines = []
        for line in delivery.lines:
            product_name = product_to_name.get(line.product_id)
            updated_line = model.DeliveryLineOut(
                **line.model_dump(), name=product_name)
            updated_lines.append(updated_line)
        salida = model.DeliveryOut(id=delivery.id,
                                   date=delivery.date,
                                   months=delivery.months,
                                   state=delivery.state,
                                   lines=updated_lines,
                                   family_id=delivery.family_id)
        result_final.append(salida)
    return result_final
