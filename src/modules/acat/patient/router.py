from typing import Any
from fastapi import APIRouter
from typing import List

from src.core.deps import SessionDep
from src.modules.acat.patient.model import Patient
from src.modules.acat.patient import controller

from src.core.deps import SessionDep

router = APIRouter()


@router.get('/')
def root():
    return 'Hello acat patient router!'


@router.post('/')
async def create_patient(session: SessionDep, patient: Patient) -> Patient:
    return await controller.create_patient_controller(session, patient)


@router.get("/")
async def get_patients(session: SessionDep) -> List:
    """Get all patients from the database."""
    return await controller.get_patients_controller(session)


 @router.get('/details/{patient_id}')
async def get_patient_details(session: SessionDep, patient_id: int) -> Any:
    return await controller.get_patient_details_controller(session, patient_id)
