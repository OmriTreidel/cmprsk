import numpy as np
import pandas as pd
import pytest

from cmprsk import utils


def get_dataframe():
    return pd.DataFrame(dict(a=[1, 2, 3], b=[1.1, 2.2, 3.3], c=['r', 's', 't']))


def test_non_numeric_columns():
    df = get_dataframe()
    assert ['c'] == utils.non_numeric_columns(df)


def test_to_categorical():
    df = get_dataframe()
    df2 = utils.to_categorical(df, ['c'])
    assert (df2['c'].values == np.arange(3)).all()
