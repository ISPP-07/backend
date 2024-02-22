from typing import Any
from fastapi import APIRouter

from src.core.deps import SessionDep
from src.modules.acat.patient.controller import get_patient_details_controller

router = APIRouter()


@router.get('/')
def root():
    return 'Hello acat patient router!'


@router.get('/details/{patient_id}')
async def get_patient_details(session: SessionDep, patient_id: int) -> Any:
    return await get_patient_details_controller(session, patient_id)
