from fastapi import APIRouter

from src.modules.shared.root import controller

router = APIRouter(
    tags=['core'],
)


@router.get('/')
def root() -> str:
    return controller.root_controller()
