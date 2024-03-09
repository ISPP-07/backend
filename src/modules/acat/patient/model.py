from typing import Optional
from datetime import date
from enum import Enum
from pydantic import BaseModel, UUID4
from src.core.database.base_crud import BaseMongo


class Gender(Enum):
    MEN = 'Men'
    WOMEN = 'Women'


class Patient(BaseMongo):
    id: UUID4
    name: str
    first_surname: str
    second_surname: Optional[str]
    alias: str  # Must be auto-generated using the name and surnames
    dni: str
    birth_date: date
    gender: Optional[Gender]
    address: Optional[str]
    contact_phone: Optional[str]
    dossier_number: str
    registration_date: date = date.today()  # Must be auto-generated
    observations: Optional[str]


class PatientCreate(BaseModel):
    name: str
    first_surname: str
    second_surname: Optional[str] = None
    dni: str
    birth_date: date
    gender: Optional[Gender] = None
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    dossier_number: str
    observations: Optional[str] = None
