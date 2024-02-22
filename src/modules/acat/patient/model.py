from typing import Optional, TYPE_CHECKING
from datetime import date
from enum import Enum
from sqlmodel import Field, String, Relationship

from src.core.database.base_crud import Base

if TYPE_CHECKING:
    from src.modules.shared.user.model import User


class Sex(str, Enum):
    MALE = 'Male'
    FEMALE = 'Female'

# This class is commented because the implementation of its functionalities will not be done in this sprint.

# class AppointmentHistory(Base, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     technician_id: Optional[int] = Field(
#         default=None,
#         foreign_key='user.id',
#     )
#     technician: Optional['User'] = Relationship()
#     technician_name: Optional[str]
#     appointment_date: date
#     patient_id: Optional[int] = Field(default=None, foreign_key='patient.id')


class PatientObservation(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    observation_text: str
    patient_id: Optional[int] = Field(default=None, foreign_key='patient.id')
    patient: Optional['Patient'] = Relationship(back_populates="observations")


class Patient(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True,)
    registration_date: date
    dossier_number: str
    name: str
    alias: str
    first_surname: str = String(length=2)
    second_surname: str = String(length=2)
    birth_date: date
    sex: Sex
    address: str
    dni: str
    contact_phone: str
    age: int
    observations: list[PatientObservation] = Relationship()
    first_appointment_date: date
    # appointment_history: list[AppointmentHistory] = Relationship(
    #     back_populates='patient_id',
    # )