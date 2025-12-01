import re
from typing import Literal

import pandas as pd

from parsers.config import config


def get_users(catalog: Literal['DATA1', 'DATA2', 'DATA3']) -> pd.DataFrame:
    users = pd.read_csv(f'data/{catalog}/users.csv', index_col=0)
    return parse_users(users)


def parse_users(users: pd.DataFrame) -> pd.DataFrame:
    users['name'] = parse_name(users['name'])
    users['email'] = parse_email(users['email'])
    users['phone'] = parse_phone(users['phone'])
    return users.convert_dtypes()


def parse_email(column: pd.Series) -> pd.Series:
    pattern = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
    return column.apply(lambda x: x if pattern.match(x) else '').astype(str)


def parse_name(column: pd.Series) -> pd.Series:
    return (
        column.fillna('')
        .str.replace(
            r'^(?:[A-Za-z ]+\. ?)?(?:Miss )?([A-Z]{1}[a-z]+) ((?:Mc|Mac|O\'|Von|Du)?[A-Z]{1}[a-z]+)(?: .+)?$',
            '\\1 \\2',
            regex=True,
        )
        .astype(str)
    )


def parse_phone(column: pd.Series) -> pd.Series:
    return (
        column.fillna('')
        .str.replace(r'[^0-9]+', '', regex=True)
        .apply(
            lambda x: f'{x[0:3]} {x[3:6]} {x[6:]}'
            if config('max_number_length') >= len(x) >= config('mix_number_length')
            else '',
        )
        .astype(str)
    )
