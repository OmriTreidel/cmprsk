import enum

import numpy as np
import pandas as pd
import rpy2 as R

from rpy2 import robjects
from pandas.api.types import is_numeric_dtype
from rpy2.robjects import r, pandas2ri, numpy2ri
from rpy2.robjects.packages import importr

pandas2ri.activate()
numpy2ri.activate()


class NotImplementedError(Exception):
    pass


class InputError(Exception):
    pass


class Dtypes(enum.Enum):
    int = R.rinterface.INTSXP
    float = R.rinterface.REALSXP
    bool = R.rinterface.LGLSXP
    str = R.rinterface.STRSXP


def r_vec(np_vec, dtype):
    return R.rinterface.SexpVector(np_vec, dtype.value)


def r_vector(np_vector):
    """Convert a numpy vector to an R vector

    Args:
        np_vector (np.array): 1 dimentional array of bool, int or floats

    Returns:
        rpy2.rinterface.SexpVector: R vector of compatible data type
    """

    if np_vector.ndim != 1:
        msg = 'Input niput dimension is %s and MUST be 1' % np_vector.ndim
        raise ValueError(msg)

    d_type = np_vector.dtype
    if np.issubdtype(d_type, np.integer):
        return r_vec(np_vector, Dtypes.int)
    elif np.issubdtype(d_type, np.floating):
        return r_vec(np_vector, Dtypes.float)
    elif np.issubdtype(d_type, np.bool):
        return r_vec(np_vector,Dtypes.bool)
    elif np.issubdtype(d_type, np.str):
        return r_vec(np_vector,Dtypes.string)
    else:
        msg = "Can't convert vectors with dtype %s yet" % d_type
        raise NotImplementedError(msg)


def r_matrix(np_matrix, col_names=None):
    """Convert a numpymatrix to R matrix. If no columns are provided
    it will assign the following ['x_1', 'x_2',... ] as column names
    """

    if np_matrix.ndim != 2:
        msg = 'Input input dimension is %s and MUST be 2' % np_matrix.ndim
        raise ValueError(msg)

    n_row, n_col = np_matrix.shape
    r_mat = robjects.r.matrix(np_matrix, nrow=n_row, ncol=n_col)
    if col_names is None:
        col_names = ['x_%s' %(i+1) for i in range(n_col)]

    r_mat.colnames = robjects.StrVector(col_names)
    return r_mat


def r_dataframe(pd_dataframe):
    return pandas2ri.py2ri(pd_dataframe)


def parse_r_list(r_list):
    return dict(zip(r_list.names, map(np.array, r_list)))
