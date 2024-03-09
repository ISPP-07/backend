from sys import maxsize
from typing import Optional, Dict, Literal, Self
from enum import Enum
from datetime import date, datetime

from fastapi import HTTPException, status
from pydantic import (
    PastDate,
    FutureDate,
    PositiveInt,
    UUID4,
    BaseModel,
    model_validator,
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


class Person(BaseModel):
    date_birth: PastDate
    type: Optional[PersonType] = None
    name: Optional[str]
    surname: Optional[str]
    nationality: Optional[str]
    nid: Optional[str]
    family_head: Optional[bool] = False
    gender: Optional[Gender]
    functional_diversity: Optional[bool] = False
    food_intolerances: list[str] = []
    homeless: Optional[bool] = False

    # HABRIA QUE CHECKEAR SI date_birth cumple el formato "%Y-%m-%d"
    # @model_validator(mode='before')
    # def validate_person(self, values: dict):
    #     if calculate_age(datetime.strptime(values['date_birth'], "%Y-%m-%d")) < 18:
    #         values['type'] = PersonType.CHILD
    #     else:
    #         values['type'] = PersonType.ADULT
    #     if values['type'] == PersonType.ADULT:
    #         if not check_nid(values['nid']):
    #             raise HTTPException(
    #                 status_code=status.HTTP_400_BAD_REQUEST,
    #                 detail={'field': 'nid', 'msg': 'Invalid NID'}
    #             )
    #         if all(values[field] is None for field in ['name', 'surname', 'nid']):
    #             raise HTTPException(
    #                 status_code=status.HTTP_400_BAD_REQUEST,
    #                 detail='Name, surname and nid are mandatory for adults'
    #             )
    #         return self
    #     else:
    #         if values['nid'] is not None:
    #             if not check_nid(values['nid']):
    #                 raise HTTPException(
    #                     status_code=status.HTTP_400_BAD_REQUEST,
    #                     detail={
    #                         'field': 'nid',
    #                         'msg': 'Invalid NID'
    #                     }
    #                 )
    #         if values['family_head']:
    #             raise HTTPException(
    #                 status_code=status.HTTP_400_BAD_REQUEST,
    #                 detail={
    #                     'field': 'family_head',
    #                     'msg': 'A child cannot be the family head'
    #                 }
    #             )
    #         return self

    def age(self) -> int:
        return calculate_age(self.date_birth)

    def age_rank(self) -> str:
        return get_age_rank(self.age)


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
    informed: bool = False
    # delivery_history: list[DeliveryHistory] = Relationship(
    #     back_populates='family_id',
    # )


# VALIDAR number_of_people == len(members), phone, que solo haya un family
# head, number_of_people se puede calcular de len(members), SI NOS DICEN
# CADA CUENTA SE TIENE QUE RENOVAR UNA FAMILIA QUITAR EL CAMPO Y AÑADIRLO
# NOSOTROS
class FamilyCreate(BaseModel):
    name: str
    phone: str
    address: str
    number_of_people: PositiveInt
    referred_organization: Optional[str] = None
    next_renewal_date: Optional[FutureDate] = None
    observation: Optional[str] = None
    members: list[Person]
