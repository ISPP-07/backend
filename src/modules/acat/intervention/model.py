from typing import Optional
from datetime import date
from pydantic import BaseModel, UUID4
from src.core.database.base_crud import BaseMongo


class Technician(BaseMongo):
    id: UUID4
    name: str
    user_id: Optional[UUID4]


class TechnicianCreate(BaseModel):
    name: str
    user_id: Optional[UUID4]


class Intervention(BaseMongo):
    id: UUID4
    date: date
    reason: Optional[str]
    typology: Optional[str]
    observations: Optional[str]
    patient_id: UUID4
    technician_id: UUID4


class InterventionCreate(BaseModel):
    date: date
    reason: Optional[str]
    typology: Optional[str]
    observations: Optional[str]
    patient_id: UUID4
    technician_id: UUID4
