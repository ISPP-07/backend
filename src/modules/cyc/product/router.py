from typing import List
from fastapi import APIRouter, status
from src.core.deps import SessionDep
from src.modules.cyc.product.controller import get_products_controller, create_product_controller, create_warehouse_controller
from src.modules.cyc.product.model import Product, Warehouse


router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK)
async def get_products(session: SessionDep) -> List[Product]:
    return await get_products_controller(session)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(session: SessionDep, product: Product) -> Product:
    return await create_product_controller(session, product)


@router.post('/warehouse', status_code=status.HTTP_201_CREATED)
async def create_warehouse(session: SessionDep, warehouse: Warehouse) -> Warehouse:
    return await create_warehouse_controller(session, warehouse)
