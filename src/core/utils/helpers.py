import argparse
from typing import Any
from datetime import date, datetime
from enum import Enum


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
            data[key] = datetime.combine(value, datetime.min.time())
        if isinstance(value, Enum):
            data[key] = value.value
        if isinstance(value, list):
            if any(isinstance(v, date) for v in value):
                value = [
                    datetime.combine(
                        item, datetime.min.time()
                    ) if isinstance(item, date) else item
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
