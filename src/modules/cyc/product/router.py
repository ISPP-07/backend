from fastapi import APIRouter, status
from src.core.deps import SessionDep
from src.modules.cyc.product.controller import create_product_controller, create_warehouse_controller
from src.modules.cyc.product.model import Product, Warehouse

router = APIRouter()


@router.post('/create')
async def create_product(session: SessionDep, product: Product, status_code=status.HTTP_201_CREATED) -> Product:
    return await create_product_controller(session, product)

@router.post('/create_warehouse')
async def create_warehouse(session: SessionDep, warehouse: Warehouse, status_code=status.HTTP_201_CREATED) -> Warehouse:
    return await create_warehouse_controller(session, warehouse)
