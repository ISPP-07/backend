from typing import Optional
from datetime import date
from enum import Enum

from pydantic import BaseModel, UUID4, PastDate

from src.core.database.base_crud import BaseMongo
from src.core.utils.helpers import calculate_age

PATIENT_NONE_FIELDS = [
    'second_surname', 'gender', 'address',
    'contact_phone', 'first_technician', 'observation'
]


class Gender(Enum):
    MEN = 'Man'
    WOMEN = 'Woman'


class Patient(BaseMongo):
    id: UUID4
    name: str
    first_surname: str
    second_surname: Optional[str]
    alias: str = None  # Must be auto-generated
    nid: str
    birth_date: PastDate
    gender: Optional[Gender]
    address: Optional[str]
    contact_phone: Optional[str]
    dossier_number: str
    is_rehabilitated: bool = False
    first_technician: Optional[str]
    registration_date: date = date.today()  # Must be auto-generated
    observation: Optional[str]

    def age(self) -> int:
        return calculate_age(self.birth_date)


class PatientCreate(BaseModel):
    name: str
    first_surname: str
    second_surname: Optional[str] = None
    alias: Optional[str] = None
    nid: str
    birth_date: PastDate
    gender: Optional[Gender] = None
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    dossier_number: str
    is_rehabilitated: bool = False
    first_technician: Optional[str] = None
    observation: Optional[str] = None


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    first_surname: Optional[str] = None
    second_surname: Optional[str] = None
    alias: Optional[str] = None
    nid: Optional[str] = None
    birth_date: Optional[PastDate] = None
    gender: Optional[Gender] = None
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    dossier_number: Optional[str] = None
    is_rehabilitated: Optional[bool] = None
    first_technician: Optional[str] = None
    registration_date: Optional[date] = None
    observation: Optional[str] = None
    update_fields_to_none: list[str] = []


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
    is_rehabilitated: bool
    registration_date: date
    first_technician: Optional[str]
    observation: Optional[str]
    age: int
