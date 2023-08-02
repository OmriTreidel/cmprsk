import numpy as np
import pandas as pd
import pytest

import cmprsk

from cmprsk import rpy_utils

def get_dataframe():
    return pd.DataFrame(dict(a=[1, 2, 3], b=[1.1, 2.2, 3.3], c=['r', 's', 't']))


class MyInt:
    def __init__(self, x):
        self.x = x

def test_all_string():
    arr = np.array(['1', 'a', '2.4'])
    assert rpy_utils.all_strings(arr)

    arr = np.array([1, 'a', 2.4])
    # implicitly converting everything to strings
    assert rpy_utils.all_strings(arr)

    arr = np.array([1, 'a', MyInt(2)])
    assert not rpy_utils.all_strings(arr)


def test_r_vector():
    np_int_vector = np.array([1, 2, 3])
    r_int_vector = rpy_utils.r_vector(np_int_vector)
    assert all(np.array(r_int_vector) == np_int_vector)

    np_float_vector = np.array([1.1, 2.1, 3.1])
    r_float_vector = rpy_utils.r_vector(np_float_vector)
    assert all(np.array(r_float_vector) == np_float_vector)

    np_bool_vector = np.array([True, False, False])
    r_bool_vector = rpy_utils.r_vector(np_bool_vector)
    assert all(np.array(r_bool_vector) == np_bool_vector)

    np_str_vector = np.array(['1', '2', '3'])
    r_str_vector = rpy_utils.r_vector(np_str_vector)
    assert all(np.array(r_str_vector) == np_str_vector)

    # works on pandas series as well
    pd_float_vector = pd.Series(np_float_vector)
    r_float_vector = rpy_utils.r_vector(np_float_vector)
    assert all(np.array(r_float_vector) == np_float_vector)

    np_convert_to_str = np.array([1, 'a', 2.4])
    r_str_vector = rpy_utils.r_vector(np_convert_to_str)
    assert all(np.array(r_str_vector) == np.array(['1', 'a', '2.4']))

    np_arr_object = np.array([1, 'a', MyInt(2)])
    with pytest.raises(rpy_utils.NotImplementedError):
        rpy_utils.r_vector(np_arr_object)


def test_r_vec():
    np_mat = np.array([[1, 2], [3, 4]])
    with pytest.raises(ValueError):
        rpy_utils.r_vector(np_mat)
