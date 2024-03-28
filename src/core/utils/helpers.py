import argparse
from typing import Any
from datetime import date, datetime
from enum import Enum

NID_LETERS = [
    'T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X',
    'B', 'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K', 'E'
]


def check_all_keys(data: dict, key: Any) -> bool:
    result = False
    for key_to_check, value in data.items():
        if key_to_check == key:
            return True
        if isinstance(value, list):
            for v in value:
                if isinstance(v, dict):
                    result = check_all_keys(v, key)
        if isinstance(value, dict):
            result = check_all_keys(value, key)
    return result


def change_invalid_types_mongo(data: dict) -> None:
    for key, value in data.items():
        if isinstance(value, date):
            data[key] = value.isoformat()
        if isinstance(value, Enum):
            data[key] = value.value
        if isinstance(value, list):
            if any(isinstance(v, date) for v in value):
                value = [
                    item.isoformat()
                    if isinstance(item, date) else item
                    for item in value
                ]
            if any(isinstance(v, Enum) for v in value):
                value = [
                    item.value if isinstance(item, Enum) else item
                    for item in value
                ]
            for v in value:
                if isinstance(v, dict):
                    change_invalid_types_mongo(v)
        if isinstance(value, dict):
            change_invalid_types_mongo(value)


def get_valid_mongo_obj(data: dict) -> dict:
    change_invalid_types_mongo(data)
    return data


def check_nid(nid: str):
    if len(nid) != 9 or not nid[:7].isdigit():
        return False
    mod = int(nid[:8]) % 23
    if nid[-1] != NID_LETERS[mod]:
        return False
    return True


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run FastAPI application with optional reload."
    )
    parser.add_argument(
        "-r",
        "--reload",
        action="store_true",
        help="Enable automatic reload"
    )
    return parser.parse_args()


def generate_alias(
        name: str,
        first_surname: str,
        second_surname: str | None) -> str:
    name_split = name.split()
    number_of_names = len(name_split)
    if number_of_names > 1:
        alias = (
            f'{name_split[0][0]}{name_split[1][0]}'
            f'{first_surname[:2]}{second_surname[:2]
                                  if second_surname is not None else ""}'
        )
    else:
        alias = (
            f'{name[:2]}{first_surname[:2]}'
            f'{second_surname[:2] if second_surname is not None else ""}'
        )
    return alias.lower()


# SOLO CALCULA LA EDAD SEGUN EL AÑO NO IMPORTA LOS MESES Y LOS DIAS
def calculate_age(birth_date: date) -> int:
    today = date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


def parse_validation_error(errors: list[dict]):
    result = ''
    for error in errors:
        result += (
            f'Field "{error["loc"]}", '
            f'error "{error["msg"]}", '
            f'with input "{error["input"]}"\n'
        )
    return result
