import numpy as np

from rpy2.robjects.packages import importr as import_R
from scipy.stats import norm as normal

from . import rpy_utils
from . import utils


r_cmprsk = import_R('cmprsk')


class NonNumericCovariateError(Exception):
    pass


class CrrResult(object):
    """An incomplete parser for the result coming from crr.

    The full result is accessible via CrrResult.raw
    """
    def __init__(self, r_crr_res):
        self.raw = r_crr_res
        self.parsed = self.asdict()
        self._coefficients = self.parsed['coef']
        self._covariance = self.parsed['var']
        self._stderr = np.sqrt(np.diag(self._covariance))

    def asdict(self):
        return rpy_utils.parse_r_list(self.raw)

    @property
    def coefficients(self):
        return self._coefficients

    @property
    def stderr(self):
        return self._stderr

    @property
    def covariance(self):
        return self._covariance

    @property
    def p_values(self):
        _p_vals = [p_value(beta, std) for beta, std in
                    zip(self.coefficients, self.stderr)]
        return np.array(_p_vals)

    @property
    def hazard_ratio(self):
        return np.exp(self._coefficients)

    def summary(self):
        print(self.raw)


def p_value(x, stderr):
    return 2 * (1 - normal.cdf(abs(x/stderr)))


def crr(ftime, fstatus, covariates_1):
    """
    Args:
        ftime (np.array): time to failure
        fstatus (np.array):
        covariates_1 (pd.DataFrame): numeric only dataframe
        # covariates_2 (pd.DataFrame): numeric only dataframe
    """
    non_numeric_cols = utils.non_numeric_columns(covariates_1)
    if non_numeric_cols:
        msg = """

        Input dataframe contains non numeric columns: {}.
        Please convert text columns using `rpy_utils.to_categorical` method first""".format(non_numeric_cols)
        raise NonNumericCovariateError(msg)

    r_cov_1 = rpy_utils.r_dataframe(covariates_1)
    r_ftime = rpy_utils.r_vector(ftime)
    r_fstatus = rpy_utils.r_vector(fstatus)
    r_crr_result = r_cmprsk.crr(r_ftime, r_fstatus, r_cov_1)
    # return r_crr_result
    return CrrResult(r_crr_result)
