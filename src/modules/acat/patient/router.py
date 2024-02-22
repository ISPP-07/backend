from typing import Any
from fastapi import APIRouter
from src.core.deps import SessionDep
from src.modules.acat.patient.controller import create_patient_controller
from src.modules.acat.patient.model import Patient

router = APIRouter()


@router.get('/')
def root():
    return 'Hello acat patient router!'

@router.post('/')
async def create_patient(session: SessionDep, patient: Patient) -> Any:
    return await create_patient_controller(session, patient)

