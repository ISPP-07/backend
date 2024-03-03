from fastapi import APIRouter
from src.modules.acat.patient import controller
from src.core.deps import SessionDep
from typing import List

router = APIRouter()


@router.get("/")
async def get_patients(session: SessionDep) -> List:
    """Get all patients from the database."""
    return await controller.get_patients_controller(session)
