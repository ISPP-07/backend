from fastapi import APIRouter, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.modules.cyc.warehouse import controller
from src.modules.cyc.warehouse.model import (
    Warehouse,
    ProductCreate,
    WarehouseCreate,
    ProductUpdate,
    ProductOut,
)


router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[Warehouse])
async def get_warehouses(db: DataBaseDep):
    return await controller.get_warehouses_controller(db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Warehouse)
async def create_warehouse(db: DataBaseDep, warehouse: WarehouseCreate):
    return await controller.create_warehouse_controller(db, warehouse)


@router.delete('/{warehouse_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_warehouse(db: DataBaseDep, warehouse_id: UUID4):
    await controller.delete_warehouse_controller(db, warehouse_id)
    return None


@router.get('/product', status_code=status.HTTP_200_OK, response_model=list[ProductOut])
async def get_products(db: DataBaseDep):
    return await controller.get_products_controller(db)


@router.post('/product', status_code=status.HTTP_201_CREATED, response_model=list[ProductOut])
async def create_product(db: DataBaseDep, product: ProductCreate):
    return await controller.create_product_controller(db, product)


@router.patch('/product', status_code=status.HTTP_200_OK, response_model=list[ProductOut])
async def update_product(db: DataBaseDep, product_update: ProductUpdate):
    return await controller.update_product_controller(db, product_update)
