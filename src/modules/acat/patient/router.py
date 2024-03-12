from fastapi import APIRouter, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.modules.acat.patient.model import Patient, PatientCreate, PatientOut
from src.modules.acat.patient import controller


router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[Patient])
async def get_patients(db: DataBaseDep):
    return await controller.get_patients_controller(db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Patient)
async def create_patient(db: DataBaseDep, patient: PatientCreate):
    return await controller.create_patient_controller(db, patient)


@router.get(
    '/{patient_id}',
    status_code=status.HTTP_200_OK,
    response_model=PatientOut
)
async def get_patient_details(db: DataBaseDep, patient_id: UUID4):
    return await controller.get_patient_details_controller(db, patient_id)
