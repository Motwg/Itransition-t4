import pandas as pd


def parse_string(column: pd.Series) -> pd.Series:
    return column.str.strip('-\n\t').fillna('').str.replace('NULL', '').astype('str')
