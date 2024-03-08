from sys import maxsize
from typing import Optional, Dict, Literal
from enum import Enum
from datetime import date, datetime
from pydantic import (
    PastDate,
    FutureDate,
    PositiveInt,
    UUID4,
    BaseModel,
    model_validator,
    ValidationError
)

from src.core.database.base_crud import BaseMongo
from src.core.utils.helpers import check_nid

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


class Gender(Enum):
    MEN = 'Men'
    WOMEN = 'Women'

# This class is commented because the implementation of its functionalities will not be done in this sprint.
# class DeliveryHistory(Base, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     delivery_date: date
#     family_id: Optional[int] = Field(default=None, foreign_key='family.id')


# VALIDAR: NID, type (lo podriamos rellenar nosotros segun la edad), validar que solo haya un family_head
class Person(BaseModel):
    date_birth: PastDate
    type: Optional[PersonType] = None
    name: Optional[str]
    surname: Optional[str]
    nationality: Optional[str]
    nid: Optional[str]
    family_head: Optional[bool] = False
    gender: Optional[Gender]
    functional_diversity: bool
    food_intolerances: list[str]
    homeless: Optional[bool] = False

    # @model_validator(mode='before')
    # @classmethod
    # def validate_person(cls, values: dict):
    #     if calculate_age(datetime.strptime(values['date_birth'], "%Y-%m-%d")) < 18:
    #         values['type'] = PersonType.CHILD
    #     else:
    #         values['type'] = PersonType.ADULT
    #     if values['type'] == PersonType.ADULT:
    #         if not check_nid(values['nid']):
    #             raise ValidationError({'field': 'nid', 'msg': 'Invalid NID'})
    #         if all(values[field] is None for field in ['name', 'surname', 'nid']):
    #             raise ValidationError(
    #                 'Name, surname and nid are mandatory for adults'
    #             )
    #     else:
    #         if values['nid'] is not None:
    #             if not check_nid(values['nid']):
    #                 raise ValidationError({
    #                     'field': 'nid',
    #                     'msg': 'Invalid NID'
    #                 })
    #         if values['family_head']:
    #             raise ValidationError({
    #                 'field': 'family_head',
    #                 'msg': 'A child cannot be the family head'
    #             })

    def age(self) -> int:
        return calculate_age(self.date_birth)

    def age_rank(self) -> str:
        return get_age_rank(self.age)


# VALIDAR number_of_people == len(members), phone, que solo haya un family head
class Family(BaseMongo):
    id: UUID4
    name: str
    phone: str
    address: str
    number_of_people: PositiveInt
    referred_organization: Optional[str]
    next_renewal_date: Optional[FutureDate]
    derecognition_state: DerecognitionStatus = DerecognitionStatus.ACTIVE
    observation: Optional[str]
    members: list[Person]
    # delivery_history: list[DeliveryHistory] = Relationship(
    #     back_populates='family_id',
    # )


class FamilyCreate(BaseModel):
    name: str
    phone: str
    address: str
    number_of_people: PositiveInt
    referred_organization: Optional[str]
    next_renewal_date: Optional[FutureDate]
    observation: Optional[str]
    members: list[Person]
