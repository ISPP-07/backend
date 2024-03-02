from typing import List
from fastapi import APIRouter
from fastapi import status
from src.core.deps import SessionDep
from src.modules.cyc.product.controller import get_products_controller
from src.modules.cyc.product.model import Product

router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK)
async def get_products(session: SessionDep) -> List[Product]:
    return await get_products_controller(session)
