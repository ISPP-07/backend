from typing import Optional
from datetime import date
from enum import Enum

from pydantic import BaseModel, UUID4, PastDate

from src.core.database.base_crud import BaseMongo
from src.core.utils.helpers import calculate_age


class Gender(Enum):
    MEN = 'Man'
    WOMEN = 'Woman'


class Patient(BaseMongo):
    id: UUID4
    name: str
    first_surname: str
    second_surname: Optional[str]
    alias: str  # Must be auto-generated using the name and surnames
    nid: str
    birth_date: PastDate
    gender: Optional[Gender]
    address: Optional[str]
    contact_phone: Optional[str]
    dossier_number: str
    first_technician: Optional[str]
    registration_date: date = date.today()  # Must be auto-generated
    observations: Optional[str]

    def age(self) -> int:
        return calculate_age(self.birth_date)


class PatientCreate(BaseModel):
    name: str
    first_surname: str
    second_surname: Optional[str] = None
    nid: str
    birth_date: PastDate
    gender: Optional[Gender] = None
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    dossier_number: str
    first_technician: Optional[str] = None
    observations: Optional[str] = None

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    first_surname: Optional[str] = None
    second_surname: Optional[str] = None
    nid: Optional[str] = None
    birth_date: Optional[PastDate] = None
    gender: Optional[Gender] = None
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    dossier_number: Optional[str] = None
    first_technician: Optional[str] = None
    observations: Optional[str] = None


class PatientOut(BaseModel):
    id: UUID4
    name: str
    first_surname: str
    second_surname: Optional[str]
    alias: str
    nid: str
    birth_date: PastDate
    gender: Optional[Gender]
    address: Optional[str]
    contact_phone: Optional[str]
    dossier_number: str
    registration_date: date
    first_technician: Optional[str]
    observations: Optional[str]
    age: int
