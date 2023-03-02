import enum

import numpy as np
import pandas as pd
import rpy2 as R
import rpy2.rinterface as rinterface

from rpy2 import robjects
from pandas.api.types import is_numeric_dtype
from rpy2.robjects import r, pandas2ri, numpy2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter


class NotImplementedError(Exception):
    pass


class InputError(Exception):
    pass

def all_strings(np_arr) -> bool:
    for x in arr:
        if not isinstance(x, str):
            return False
    return True


def r_vector(np_vector):
    """Convert a numpy vector to an R vector

    Args:
        np_vector (np.array): 1 dimenssional array of bool, int or floats

    Returns:
        rpy2.rinterface.SexpVector: R vector of compatible data type
    """

    if np_vector.ndim != 1:
        msg = 'Input niput dimension is %s and MUST be 1' % np_vector.ndim
        raise ValueError(msg)

    d_type = np_vector.dtype
    if np.issubdtype(d_type, np.integer):
        return rinterface.IntSexpVector(np_vector)
    elif np.issubdtype(d_type, np.floating):
        return rinterface.FloatSexpVector(np_vector)
    elif np.issubdtype(d_type, bool):
        return rinterface.BoolSexpVector(np_vector)
    elif np.issubdtype(d_type, str):
        return rinterface.StrSexpVector(np_vector)
    elif all_strings(np_vector):
        # this is an expensive check. However unless dtype is explicitly set to str numpy array of strings have dtype 'O'
        return rinterface.StrSexpVector(np_vector)
    else:
        msg = "Can't convert vectors with dtype %s yet" % d_type
        raise NotImplementedError(msg)


def r_dataframe(pd_dataframe):
    with localconverter(robjects.default_converter + pandas2ri.converter):
        return robjects.conversion.py2rpy(pd_dataframe)


def pandas_dataframe(r_dataframe):
    with localconverter(robjects.default_converter + pandas2ri.converter):
        return robjects.conversion.rpy2py(r_dataframe)


def parse_r_list(r_list):
    return dict(zip(r_list.names, np.array(r_list, dtype=object)))
