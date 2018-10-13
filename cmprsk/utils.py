import pandas as pd

from pandas.api.types import is_numeric_dtype


def to_categorical(df, columns):
    """ Creates a COPY and replace the text columns integer values (categories)

    Args:
        df: some data frame
        columns: list of TEXT columns to be interperted as categories

    Returns:
        a copy dataframe with TEXT columns replaced with intgers
    """
    _df = df.copy()
    for c in columns:
        _df.loc[:, c] = df[c].astype('category').cat.codes
    return _df


def non_numeric_columns(df):
    """ Returns a listof non numeric columns """
    return [c for c in df.columns if not is_numeric_dtype(df[c])]
