import argparse
import re
from itertools import combinations
from typing import Any
from datetime import date
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


def change_invalid_types_mongo(data: dict | list) -> None:
    if isinstance(data, list):
        for item in data:
            if isinstance(item, date):
                item = item.isoformat()
            if isinstance(item, Enum):
                item = item.value
            if isinstance(item, dict) or isinstance(item, list):
                change_invalid_types_mongo(item)
    else:
        for key, value in data.items():
            if isinstance(value, date):
                data[key] = value.isoformat()
            if isinstance(value, Enum):
                data[key] = value.value
            if isinstance(value, dict) or isinstance(value, list):
                change_invalid_types_mongo(value)


def get_valid_mongo_obj(data: dict | list) -> dict | list:
    change_invalid_types_mongo(data)
    return data


def check_nid(data: str):
    nif_pattern = re.compile('^[0-9]{8}[TRWAGMYFPDXBNJZSQVHLCKE]$')
    nie_pattern = re.compile('^[XYZ][0-9]{7}[TRWAGMYFPDXBNJZSQVHLCKE]$')
    if not nif_pattern.match(data) and not nie_pattern.match(data):
        return False
    nie = re.sub(
        '^[X]', '0',
        re.sub('^[Y]', '1', re.sub('^[Z]', '2', data))
    )
    mod = int(nie[:8]) % 23
    if data[-1] != NID_LETERS[mod]:
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
            f'{first_surname[:2]}'
            f'{second_surname[:2] if second_surname is not None else ""}'
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


def get_all_combinations(data: list):
    result = list()
    for n in range(1, len(data) + 1):
        result += list(combinations(data, n))
    return result
