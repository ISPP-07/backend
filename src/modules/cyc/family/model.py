from sys import maxsize
from typing import Optional, Dict, Literal
from enum import Enum
from datetime import date
from sqlmodel import Field, Relationship
from pydantic import PositiveInt

from src.core.database.base_crud import Base

AGE_RANGES: Dict[
    Literal['baby', 'child', 'adult', 'senior', 'old'],
    Dict[Literal['min', 'max'], int]
] = {
    'baby': {'min': 0, 'max': 3, },
    'child': {'min': 3, 'max': 15, },
    'adult': {'min': 15, 'max': 45, },
    'senior': {'min': 45, 'max': 60, },
    'old': {'min': 60, 'max': maxsize, },
}


def calculate_age(birth_date: date) -> int:
    today = date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


def get_age_rank(age: int) -> str:
    for key, entry in AGE_RANGES.items():
        if entry.get('min') < age <= entry.get('max'):
            return key
    raise ValueError('Age cannot be negative')


class DerecognitionStatus(str, Enum):
    ACTIVE = 'Active'
    SUSPENDED = 'Suspended'


# This class is commented because the implementation of its functionalities will not be done in this sprint.
# class DeliveryHistory(Base, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     delivery_date: date
#     family_id: Optional[int] = Field(default=None, foreign_key='family.id')


class FamilyObservation(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    observation_text: str
    family_id: Optional[int] = Field(default=None, foreign_key='family.id')
    family: 'Family' = Relationship(back_populates='observations')


# POR AHORA LO HE RELACIONADO COMO 1-* PERO PODRIA SER *-*
# SI UN MISMO PRODUCTO LO GUARDAN EN ALMACENES DIFERENTES
class Product(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    quantity: PositiveInt
    exp_date: Optional[date]
    warehouse_id: Optional[int] = Field(
        default=None, foreign_key='warehouse.id'
    )
    warehouse: 'Warehouse' = Relationship(back_populates='products')


class Warehouse(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    products: list[Product] = Relationship(back_populates='warehouse')


class Person(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date_birth: date
    type: str
    name: Optional[str]
    dni: Optional[str]
    family_id: Optional[int] = Field(default=None, foreign_key='family.id')
    family: 'Family' = Relationship(back_populates='persons')

    def age(self) -> int:
        return calculate_age(self.date_birth)

    def age_rank(self) -> str:
        return get_age_rank(self.age)


class Family(Base, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    phone: str
    address: str
    number_of_people: int
    referred_organization: str
    next_renewal_date: date
    derecognition_state: DerecognitionStatus
    observations: list[FamilyObservation] = Relationship(
        back_populates='family'
    )
    persons: list[Person] = Relationship(back_populates='family')
    # delivery_history: list[DeliveryHistory] = Relationship(
    #     back_populates='family_id',
    # )