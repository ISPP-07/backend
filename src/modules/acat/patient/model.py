from typing import Optional
from datetime import date
from enum import Enum
from sqlmodel import Field, String, Relationship

from src.core.database.base_crud import Base


class Technician(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    user_id: Optional[int] = Field(
        default=None,
        foreign_key='user.id',
    )
    appointments: list['Appointment'] = Relationship(
        back_populates='technician'
    )


class Sex(str, Enum):
    MALE = 'Male'
    FEMALE = 'Female'


class Appointment(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    technician_id: Optional[int] = Field(
        default=None,
        foreign_key='technician.id',
    )
    technician: Technician = Relationship(back_populates='appointments')
    appointment_date: date
    patient_id: Optional[int] = Field(default=None, foreign_key='patient.id')
    patient: 'Patient' = Relationship(back_populates='appointments')


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
    observations: list[PatientObservation] = Relationship(
        back_populates='patient'
    )
    first_appointment_date: date
    appointments: list[Appointment] = Relationship(
        back_populates='patient',
    )
