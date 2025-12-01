import re
from typing import Literal

import pandas as pd

from parsers.config import config
from parsers.generic import parse_string


def get_orders(catalog: Literal['DATA1', 'DATA2', 'DATA3']) -> pd.DataFrame:
    orders = pd.read_parquet(f'data/{catalog}/orders.parquet')
    orders = orders.set_index('id')
    orders = parse_orders(orders)
    orders['paid_price'] = orders['quantity'] * orders['unit_price']
    return orders


def parse_orders(orders: pd.DataFrame) -> pd.DataFrame:
    for col in ['shipping', 'timestamp', 'unit_price']:
        orders[col] = parse_string(orders[col])
    orders['quantity'] = parse_quantity(orders['quantity'])
    orders['unit_price'] = parse_unit_price(orders['unit_price'])
    orders['timestamp'] = parse_timestamp(orders['timestamp'])
    orders['date'] = parse_date(orders['timestamp'])
    return orders.convert_dtypes()


def parse_quantity(quantity: pd.Series) -> pd.Series:
    return (
        pd.to_numeric(quantity, errors='coerce')
        .apply(lambda x: x if x > 0 else pd.NA)
        .astype('Int64')
    )


def parse_timestamp(timestamp: pd.Series) -> pd.Series:
    return pd.to_datetime(
        timestamp.str.upper().str.replace(',', ' ').str.replace('.M.', 'M'), format='mixed'
    )


def parse_date(timestamp: pd.Series) -> pd.Series:
    return timestamp.dt.date.astype('str')


def parse_unit_price(unit_price: pd.Series) -> pd.Series:
    def currency_mult(row: str) -> int:
        mult = 100
        if '€' in row or 'EUR' in row:
            mult *= config('eur_to_usd')
        value = float('{}.{}'.format(*re.findall(r'(\d+)(?:[^\d])?(\d{1,2})?', row)[0]))
        return int(value * mult)

    return pd.to_numeric(unit_price.apply(currency_mult))
