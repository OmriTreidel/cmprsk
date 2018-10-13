import pandas as pd

from cmprsk import utils


def get_dataframe():
    return pd.DataFrame(dict(a=[1, 2, 3], b=[1.1, 2.2, 3.3], c=['r', 's', 't']))


def test_non_numeric_columns():
    df = get_dataframe()
    assert ['c'] == utils.non_numeric_columns(df)
