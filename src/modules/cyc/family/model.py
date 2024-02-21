from typing import Optional
from enum import Enum
from datetime import date
from sqlmodel import Field, Relationship

from src.core.database.base_crud import Base


class DerecognitionStatus(str, Enum):
    ACTIVE = 'Active'
    SUSPENDED = 'Suspended'


class AgeRange(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    MinAge: int
    MaxAge: int


class FamilyAgeRangeLink(Base, table=True):
    family_id: Optional[int] = Field(
        default=None,
        foreign_key='family.id',
        primary_key=True,
    )
    age_range_id: Optional[int] = Field(
        default=None,
        foreign_key='agerange.id',
        primary_key=True,
    )


# This class is commented because the implementation of its functionalities will not be done in this sprint.

# class DeliveryHistory(Base, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     delivery_date: date
#     family_id: Optional[int] = Field(default=None, foreign_key='family.id')


class FamilyObservation(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    observation_text: str
    family_id: Optional[int] = Field(default=None, foreign_key='family.id')
    family: Optional['Family'] = Relationship(back_populates='observations')


class Family(Base, table=True):
    id: int = Field(default=None, primary_key=True,)
    name: str
    phone: str
    address: str
    age_ranges: list[AgeRange] = Relationship(link_model=FamilyAgeRangeLink)
    number_of_people: int
    referred_organization: str
    next_renewal_date: date
    derecognition_state: DerecognitionStatus
    observations: list[FamilyObservation] = Relationship(
        back_populates='family'
    )
    # delivery_history: list[DeliveryHistory] = Relationship(
    #     back_populates='family_id',
    # )