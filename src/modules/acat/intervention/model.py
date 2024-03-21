from typing import Optional
from datetime import date
from pydantic import BaseModel, UUID4, FutureDate

from src.core.database.base_crud import BaseMongo
from src.modules.acat.patient.model import Patient


class Intervention(BaseMongo):
    id: UUID4
    date: date
    reason: Optional[str]
    typology: Optional[str]
    observations: Optional[str]
    technician: str
    patient: Patient


class InterventionCreate(BaseModel):
    date: date
    reason: Optional[str] = None
    typology: Optional[str] = None
    observations: Optional[str] = None
    patient_id: UUID4
    technician: str


class InterventionUpdate(BaseModel):
    date: Optional[FutureDate] = None
    reason: Optional[str] = None
    typology: Optional[str] = None
    observations: Optional[str] = None
    patient_id: Optional[UUID4] = None
    technician: Optional[str] = None
