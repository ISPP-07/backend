from typing import Any
from fastapi import APIRouter
from typing import List

from src.core.deps import SessionDep
from src.modules.acat.patient.controller import create_patient_controller
from src.modules.acat.patient.model import Patient
from src.modules.acat.patient import controller

router = APIRouter()


@router.get('/')
def root():
    return 'Hello acat patient router!'


@router.post('/')
async def create_patient(session: SessionDep, patient: Patient) -> Patient:
    return await create_patient_controller(session, patient)

@router.get("/")
async def get_patients(session: SessionDep) -> List:
    """Get all patients from the database."""
    return await controller.get_patients_controller(session)

