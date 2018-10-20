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


def _to_dummies(df, column_name, base=None):
    _df = df.copy()
    _dummies = pd.get_dummies(df[column_name], prefix=column_name).astype('int64')
    if base is not None:
        _dummies = _dummies.drop('%s_%s' % (column_name, base), axis=1)

    _df = _df.drop(column_name, axis=1)
    return pd.concat([_df, _dummies], axis=1)


def as_indicators(df, column_names, bases=None):
    if bases is None:
        bases = [None] * len(column_names)

    _df = df.copy()
    for col, base in zip(column_names, bases):
        _df = _to_dummies(_df, col, base=base)

    return _df
