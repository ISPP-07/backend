from fastapi import APIRouter
from src.modules.shared.auth import controller

router = APIRouter(
    tags=['core'],
)


@router.get('/')
def root():
    return controller.root_controller()


@router.get('/hello')
def hello():
    return controller.hello_controller()
