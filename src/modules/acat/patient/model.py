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


class AppointmentHistory(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    appointment_date: date
    patient_id: Optional[int] = Field(default=None, foreign_key='patient.id')


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
    observations: str
    first_appointment_date: date
    attending_technician_id: Optional[int] = Field(
        default=None,
        foreign_key='user.id',
    )
    attending_technician: Optional['User'] = Relationship()
    attending_technician_name: Optional[str]
    appointment_history: list[AppointmentHistory] = Relationship(
        back_populates='patient_id',
    )
