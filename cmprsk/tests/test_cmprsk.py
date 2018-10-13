import numpy as np
import pandas as pd
import pytest
import random
import string


import cmprsk.cmprsk as cmprsk

from cmprsk import utils


def get_data():
    np.random.seed(42)
    ftime = np.random.exponential(size=200)
    fstatus = np.random.randint(0, 3, 200)
    x2 = np.random.exponential(size=200)
    x3 = np.random.randn(200)
    x1 = [random.choice(string.ascii_lowercase) for _ in range(200)]
    cov = pd.DataFrame(dict(x1=x1, x2=x2, x3=x3))
    return ftime, fstatus, cov


def test_cmprsk():
    ftime, fstatus, cov = get_data()

    with pytest.raises(cmprsk.NonNumericCovariateError):
        cmprsk.crr(ftime, fstatus, cov)

    cov_1 = utils.to_categorical(cov, ['x1'])
    crr_res = cmprsk.crr(ftime, fstatus, cov_1)
    assert isinstance(crr_res, cmprsk.CrrResult)

# try:
#     cov_2 = to_categorical(cov, ['x0'])
#     res = R_crr(ftime, fstatus, cov_2)
#     print(res.raw)
# except Exception as exc:
#     print(exc)
#
# try:
#     res = R_crr(ftime, fstatus, cov)
# except InputError as exc:
#     print("caught the right exception")
#     print(exc)
