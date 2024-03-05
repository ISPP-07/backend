from sys import maxsize
from typing import Optional, Dict, Literal
from enum import Enum
from uuid import UUID
from datetime import date
from pydantic import PastDate, FutureDate, PositiveInt

from src.core.database.base_crud import BaseMongo

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


class DerecognitionStatus(Enum):
    ACTIVE = 'Active'
    SUSPENDED = 'Suspended'


class PersonType(Enum):
    CHILD = 'Child'
    ADULT = 'Adult'

# This class is commented because the implementation of its functionalities will not be done in this sprint.
# class DeliveryHistory(Base, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     delivery_date: date
#     family_id: Optional[int] = Field(default=None, foreign_key='family.id')


class Person(BaseMongo, table=True):
    id: UUID
    date_birth: PastDate
    type: PersonType
    name: Optional[str]
    nid: Optional[str]
    family_head: bool = False
    family_id: UUID

    def age(self) -> int:
        return calculate_age(self.date_birth)

    def age_rank(self) -> str:
        return get_age_rank(self.age)


class Family(BaseMongo):
    id: UUID
    name: str
    phone: str
    address: str
    number_of_people: PositiveInt
    referred_organization: str
    next_renewal_date: FutureDate
    derecognition_state: DerecognitionStatus
    observation: str
    # delivery_history: list[DeliveryHistory] = Relationship(
    #     back_populates='family_id',
    # )


class FamilyWithMembers(Family):
    members: list[Person]
