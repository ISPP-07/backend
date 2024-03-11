from typing import Optional
from datetime import date
from pydantic import BaseModel, UUID4

from src.core.database.base_crud import BaseMongo
from src.modules.acat.patient.model import Patient


class Intervention(BaseMongo):
    id: UUID4
    date: date
    reason: Optional[str]
    typology: Optional[str]
    observations: Optional[str]
    patient: Patient
    technician: str


class InterventionCreate(BaseModel):
    date: date
    reason: Optional[str] = None
    typology: Optional[str] = None
    observations: Optional[str] = None
    patient_id: UUID4
    technician: str
