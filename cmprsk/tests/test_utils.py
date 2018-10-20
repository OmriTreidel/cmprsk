import numpy as np
import pandas as pd
import pytest

from cmprsk import utils


def get_dataframe():
    return pd.DataFrame(dict(a=[2, 2, 0, 2, 0],
                             b=[1.1, 2.2, 3.3, 4, 5],
                             c=['r', 's', 't', 't', 'r']))


def test_non_numeric_columns():
    df = get_dataframe()
    assert ['c'] == utils.non_numeric_columns(df)


def test_to_categorical():
    df = get_dataframe()
    df2 = utils.to_categorical(df, ['c'])
    assert (df2['c'].values == np.array([0, 1, 2, 2, 0])).all()


def test_dummies():
    df = get_dataframe()
    _df = utils._to_dummies(df, 'c', base='t')
    expected = df[['a', 'b']]
    expected['c_r'] = [1, 0, 0, 0, 1]
    expected['c_s'] = [0, 1, 0, 0, 0]
    assert (_df.columns == expected.columns).all()
    assert (_df.values == expected.values).all

    _df = utils._to_dummies(df, 'c')
    expected = df[['a', 'b']]
    expected['c_r'] = [1, 0, 0, 0, 1]
    expected['c_s'] = [0, 1, 0, 0, 0]
    expected['c_t'] = [0, 0, 1, 1, 0]
    assert (_df.columns == expected.columns).all()
    assert (_df.values == expected.values).all


def test_as_indicators():
    df = get_dataframe()
    _df = utils.as_indicators(df, ['a', 'c'], bases=[2, 't'])
    expected = df[['b']]
    expected['a_0'] = [0, 0, 1, 0, 1]
    expected['c_r'] = [1, 0, 0, 0, 1]
    expected['c_s'] = [0, 1, 0, 0, 0]
    assert (_df.columns == expected.columns).all()
    assert (_df.values == expected.values).all
