import numpy as np
import pandas as pd
import pytest
import random
import string


import cmprsk.cmprsk as cmprsk

from cmprsk import utils


def get_data():
    np.random.seed(42)
    random.seed(34)
    ftime = np.random.exponential(size=200)
    fstatus = pd.Series(np.random.randint(0, 3, 200))
    x2 = np.random.exponential(size=200)
    x3 = np.random.randn(200)
    x1 = [random.choice(string.ascii_lowercase) for _ in range(200)]
    x4 = np.random.randint(0, 10, 200).astype(int)
    cov = pd.DataFrame(dict(x1=x1, x2=x2, x3=x3, x4=x4))
    return ftime, fstatus, cov


def test_crr():
    ftime, fstatus, cov = get_data()

    with pytest.raises(cmprsk.NonNumericCovariateError):
        cmprsk.crr(ftime, fstatus, cov)

    cov_1 = utils.as_indicators(cov, ['x1', 'x4'], bases=['d', 5])
    crr_res = cmprsk.crr(ftime, fstatus, cov_1)
    report = crr_res.summary
    assert isinstance(crr_res, cmprsk.CrrResult)


def test_cuminc():
    ftime, fstatus, _ = get_data()
    crr_res = cmprsk.cuminc(ftime, fstatus)
    assert isinstance(crr_res, cmprsk.CumincResult)
