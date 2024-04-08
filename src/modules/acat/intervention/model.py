from typing import Optional
from datetime import datetime

from pydantic import BaseModel, UUID4, NonNegativeInt
from src.core.database.base_crud import BaseMongo
from src.modules.acat.patient.model import Patient

INTERVENTION_NONE_FIELDS = [
    'reason', 'typology', 'observations'
]


class Intervention(BaseMongo):
    id: UUID4
    date: datetime
    reason: Optional[str]
    typology: Optional[str]
    observations: Optional[str]
    technician: str
    patient: Patient


class InterventionCreate(BaseModel):
    date: datetime
    reason: Optional[str] = None
    typology: Optional[str] = None
    observations: Optional[str] = None
    patient_id: UUID4
    technician: str


class InterventionUpdate(BaseModel):
    date: Optional[datetime] = None
    reason: Optional[str] = None
    typology: Optional[str] = None
    observations: Optional[str] = None
    patient_id: Optional[UUID4] = None
    technician: Optional[str] = None
    update_fields_to_none: list[str] = []


class GetInterventions(BaseModel):
    elements: list[Intervention]
    total_elements: NonNegativeInt
