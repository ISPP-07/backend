from typing import Optional, TYPE_CHECKING
from datetime import date
from sqlmodel import Field, Relationship

from src.core.database.base_crud import Base

if TYPE_CHECKING:
    from src.modules.acat.patient.model import Technician, Patient


class Appointment(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    technician_id: Optional[int] = Field(
        default=None,
        foreign_key='technician.id',
    )
    technician: 'Technician' = Relationship(back_populates='appointments')
    appointment_date: date
    patient_id: Optional[int] = Field(default=None, foreign_key='patient.id')
    patient: 'Patient' = Relationship(back_populates='appointments')
