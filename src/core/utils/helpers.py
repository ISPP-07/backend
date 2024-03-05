from typing import Any


def check_all_keys(element: dict, key: Any) -> bool:
    for key_to_check, value in element.items():
        if key_to_check == key:
            return True
        if isinstance(value, dict):
            return check_all_keys(value, key)
    return False
