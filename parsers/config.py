from typing import Any


def config(key: str) -> Any:
    return {
        'prelease_month_limit': 1,
        'max_number_length': 11,
        'min_number_length': 8,
        'eur_to_usd': 1.2,
    }.get(key)
