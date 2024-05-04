from typing import Optional, Self
from datetime import date
from enum import Enum

from pydantic import BaseModel, UUID4, PastDate, NonNegativeInt, model_validator
from fastapi import HTTPException, status

from src.core.database.base_crud import BaseMongo
from src.core.utils.helpers import calculate_age, check_nid

PATIENT_NONE_FIELDS = [
    'second_surname', 'gender', 'address',
    'contact_phone', 'first_technician', 'observation'
]


class Gender(Enum):
    MEN = 'Man'
    WOMEN = 'Woman'


class PatientValidation():
    @classmethod
    def validate_nid(cls, data: Self):
        if not check_nid(data.nid):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'NID with value {data.nid} is invalid'
            )
        return data


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


class PatientCreate(BaseModel, PatientValidation):
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

    @model_validator(mode='after')
    @classmethod
    def validate_patient_create(cls, data: Self):
        cls.validate_nid(data)
        return data


class PatientUpdate(BaseModel, PatientValidation):
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

    @model_validator(mode='after')
    @classmethod
    def validate_patient_update(cls, data: Self):
        cls.validate_nid(data)
        return data


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


class GetPatients(BaseModel):
    elements: list[Patient]
    total_elements: NonNegativeInt
