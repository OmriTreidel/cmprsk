import numpy as np
import pandas as pd
import pytest

import cmprsk

from cmprsk import rpy_utils
from cmprsk.rpy_utils import Dtypes


def get_dataframe():
    return pd.DataFrame(dict(a=[1, 2, 3], b=[1.1, 2.2, 3.3], c=['r', 's', 't']))


def test_r_vec():
    np_int_vector = np.array([1, 2, 3])
    r_int_vector = rpy_utils.r_vec(np_int_vector, Dtypes.int)
    assert (np.array(r_int_vector) == np_int_vector).all()

    np_float_vector = np.array([1.1, 2.1, 3.1])
    r_float_vector = rpy_utils.r_vec(np_float_vector, Dtypes.float)
    assert (np.array(r_float_vector) == np_float_vector).all()

    np_bool_vector = np.array([True, True, False])
    r_bool_vector = rpy_utils.r_vec(np_bool_vector, Dtypes.bool)
    assert (np.array(r_bool_vector) == np_bool_vector).all()

    np_str_vector = np.array(['a', 'b', 'c'])
    r_str_vector = rpy_utils.r_vec(np_str_vector, Dtypes.str)
    assert (np.array(r_str_vector) == np_str_vector).all()

    np_mat = np.array([[1, 2], [3, 4]])
    with pytest.raises(ValueError):
        rpy_utils.r_vector(np_mat)

def test_r_matrix():
    np_mat = np.array([[1, 2], [3, 4]])
    r_mat = rpy_utils.r_matrix(np_mat)
    assert (np_mat == np.array(r_mat)).all()
    assert (np.array(r_mat.colnames) == np.array(['x_1', 'x_2'])).all()
