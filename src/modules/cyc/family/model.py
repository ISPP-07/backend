from src.core.utils.helpers import check_nid, calculate_age
from src.core.database.base_crud import BaseMongo
from fastapi import HTTPException, status
from sys import maxsize
from typing import Optional, Dict, Literal, Self
from enum import Enum
from datetime import date
from pydantic import (
    PastDate,
    FutureDate,
    PositiveInt,
    NonNegativeInt,
    UUID4,
    BaseModel,
    model_validator,
)

FAMILY_NONE_FIELDS = [
    'referred_organization', 'next_renewal_date', 'observation'
]


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

PERSON_NONE_FIELDS = [
    'type', 'name', 'surname', 'nationality',
    'nid', 'gender', 'functional_diversity', 'homeless'
]


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
    MEN = 'Man'
    WOMEN = 'Woman'

# This class is commented because the implementation of its functionalities
# will not be done in this sprint.
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
    nid: str
    family_head: bool = False
    gender: Optional[Gender]
    functional_diversity: Optional[bool] = False
    food_intolerances: list[str] = []
    homeless: Optional[bool] = False

    @model_validator(mode='after')
    @classmethod
    def validate_person(cls, data: Self):
        if calculate_age(data.date_birth) < 18:
            data.type = PersonType.CHILD
        else:
            data.type = PersonType.ADULT
        if data.type == PersonType.ADULT:
            if not check_nid(data.nid):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={'field': 'nid', 'msg': 'Invalid NID'}
                )
            if all(
                data.__dict__[field] is None for field in [
                    'name',
                    'surname',
                    'nid']):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Name, surname and nid are mandatory for adults'
                )
            return data
        else:
            if data.nid is not None:
                if not check_nid(data.nid):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            'field': 'nid',
                            'msg': 'Invalid NID'
                        }
                    )
            if data.family_head:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        'field': 'family_head',
                        'msg': 'A child cannot be the family head'
                    }
                )
            return data

    def age(self) -> int:
        return calculate_age(self.date_birth)

    def age_rank(self) -> str:
        return get_age_rank(self.age)


class PersonUpdate(BaseModel):
    date_birth: Optional[PastDate] = None
    type: Optional[PersonType] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    nationality: Optional[str] = None
    nid: Optional[str] = None
    gender: Optional[Gender] = None
    functional_diversity: Optional[bool] = None
    food_intolerances: Optional[list[str]] = None
    homeless: Optional[bool] = None
    update_fields_to_none: list[str] = []


class FamilyValidator:
    @classmethod
    def validate_family_members(cls, members: list['Person']):
        if len(members) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    'field': 'members',
                    'msg': 'A family must have at least one member'
                }
            )
        check_family_head = list(filter(
            lambda p: p.family_head,
            members
        ))
        if len(check_family_head) != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    'field': 'members',
                    'msg': 'A family can only have one head of household'
                }
            )


class Family(BaseMongo, FamilyValidator):
    id: UUID4
    name: str
    phone: str
    address: str
    referred_organization: Optional[str]
    next_renewal_date: Optional[date]
    derecognition_state: DerecognitionStatus = DerecognitionStatus.ACTIVE
    observation: Optional[str]
    number_of_people: PositiveInt = None
    informed: bool = False
    members: list[Person]
    # delivery_history: list[DeliveryHistory] = Relationship(
    #     back_populates='family_id',
    # )

    @model_validator(mode='after')
    @classmethod
    def validate_family(cls, data: 'Self'):
        cls.validate_family_members(data.members)
        data.number_of_people = len(data.members)
        return data

# VALIDAR phone, SI NOS DICEN CADA CUENTA SE TIENE QUE RENOVAR UNA FAMILIA QUITAR
# EL CAMPO Y AÑADIRLO NOSOTROS


class FamilyCreate(BaseModel):
    name: str
    phone: str
    address: str
    referred_organization: Optional[str] = None
    next_renewal_date: Optional[FutureDate] = None
    observation: Optional[str] = None
    members: list[Person]


class FamilyUpdate(BaseModel, FamilyValidator):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    referred_organization: Optional[str] = None
    next_renewal_date: Optional[FutureDate] = None
    derecognition_state: Optional[DerecognitionStatus] = None
    observation: Optional[str] = None
    number_of_people: Optional[PositiveInt] = None
    informed: Optional[bool] = None
    members: Optional[list[Person]] = None
    update_fields_to_none: list[str] = []

    @model_validator(mode='after')
    @classmethod
    def validate_family_update(cls, data: 'Self'):
        if data.members is not None:
            cls.validate_family_members(data.members)
            data.number_of_people = len(data.members)
        return data
    observation: Optional[str] = None
    members: Optional[list[Person]] = None


class GetFamilies(BaseModel):
    elements: list[Family]
    total_elements: NonNegativeInt
