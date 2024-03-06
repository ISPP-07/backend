from fastapi import APIRouter, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.modules.cyc.product import controller
from src.modules.cyc.product.model import (
    Product,
    Warehouse,
    ProductCreate,
    WarehouseCreate,
    ProductUpdate
)


router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[Product])
async def get_products(db: DataBaseDep):
    return await controller.get_products_controller(db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Product)
async def create_product(db: DataBaseDep, product: ProductCreate):
    return await controller.create_product_controller(db, product)


@router.post('/warehouse', status_code=status.HTTP_201_CREATED, response_model=Warehouse)
async def create_warehouse(db: DataBaseDep, warehouse: WarehouseCreate):
    return await controller.create_warehouse_controller(db, warehouse)


@router.get('/warehouse', status_code=status.HTTP_200_OK, response_model=list[Warehouse])
async def get_warehouses(db: DataBaseDep):
    return await controller.get_warehouses_controller(db)


@router.patch('/{product_id}', status_code=status.HTTP_200_OK, response_model=Product)
async def update_product(db: DataBaseDep, product_id: UUID4, product_update: ProductUpdate):
    return await controller.update_product_controller(db, product_id, product_update)


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_product(db: DataBaseDep, product_id: UUID4):
    await controller.delete_product_controller(db, product_id)
    return None
