from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd
import yaml
from dateutil.relativedelta import relativedelta

from parsers.config import parser_config
from parsers.generic import parse_string
from parsers.users import parse_name


def get_books(catalog: Literal['DATA1', 'DATA2', 'DATA3']) -> pd.DataFrame:
    with Path(f'data/{catalog}/books.yaml').open() as file:
        books = pd.DataFrame(yaml.safe_load(file))
    books = books.rename(
        columns={
            ':id': 'id',
            ':title': 'title',
            ':author': 'author',
            ':genre': 'genre',
            ':publisher': 'publisher',
            ':year': 'year',
        },
    )
    books = books.set_index('id')
    return parse_books(books)


def parse_books(books: pd.DataFrame) -> pd.DataFrame:
    for col in ['title', 'author', 'genre', 'publisher']:
        books[col] = parse_string(books[col])
        books['year'] = parse_year(books['year'])
        books['author'] = parse_author(books['author'])
    return books.convert_dtypes()


def parse_author(author: pd.Series) -> pd.Series:
    return (
        author.str.split(', ', expand=True)
        .apply(parse_name)
        .apply(
            lambda row: ', '.join(np.sort((x := row.to_numpy().astype(str))[x != ''])),
            axis=1,
        )
    )


def parse_year(year: pd.Series) -> pd.Series:
    return (
        pd.to_numeric(year, errors='coerce')
        .apply(
            lambda y: y
            if int(
                (
                    datetime.now(tz=UTC).date()
                    + relativedelta(months=+(parser_config('prelease_month_limit')))
                ).strftime('%Y'),
            )
            >= y
            > 0
            else pd.NA,
        )
        .astype('Int64')
    )
