from typing import Any
from fastapi import APIRouter
from typing import List

from src.core.deps import DataBaseDep
from src.modules.acat.patient.model import Patient
from src.modules.acat.patient import controller

router = APIRouter()


@router.post('/')
async def create_patient(db: DataBaseDep, patient: Patient) -> Patient:
    return await controller.create_patient_controller(db, patient)


@router.get("/")
async def get_patients(db: DataBaseDep) -> List:
    """Get all patients from the database."""
    return await controller.get_patients_controller(db)


@router.get('/details/{patient_id}')
async def get_patient_details(db: DataBaseDep, patient_id: int) -> Any:
    return await controller.get_patient_details_controller(db, patient_id)
