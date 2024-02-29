from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import date


class TechnicianRead(SQLModel):
    name: str


class PatientRead(SQLModel):
    name: str
    birth_date: date


class AppointmentRead(SQLModel):
    appointment_date: date
    technician: Optional[TechnicianRead] = None
    patient: Optional[PatientRead] = None
