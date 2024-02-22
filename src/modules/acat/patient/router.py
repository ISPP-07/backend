from fastapi import APIRouter
from src.modules.acat.patient import controller
from src.core.deps import SessionDep
from typing import Any

router = APIRouter()


@router.get('/')
def root():
    return 'Hello acat patient router!'

@router.get("/list")
async def get_patients(session: SessionDep) -> Any:
    """Get all patients from the database."""
    return await controller.get_patients_controller(session)
