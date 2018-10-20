import numpy as np
import pandas as pd

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
        self._z = self._covariance/self._stderr

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

    def hazard_ratio(self, conf_level=0.95):
        values = np.zeros(len(self.coefficients))
        confidence = np.zeros((len(self.coefficients), 2))
        edges = np.array(normal.interval(conf_level))
        for i, (coef, std) in enumerate(zip(self.coefficients, self.stderr)):
            values[i] = np.exp(coef)
            confidence[i, :] = [np.exp(coef + edges[0] * std),
                                np.exp(coef + edges[1] * std)]
        return values, confidence

    def summary(self):
        print(self.raw)


def p_value(x, stderr):
    return 2 * (1 - normal.cdf(abs(x/stderr)))


def crr(ftime, fstatus, static_covariates, cengroup=None, failcode=1, cencode=0,
        subset=None, **kwargs):
    """
    Args:
        ftime (np.array or pandas.Series): time to failure
        fstatus (np.array or pandas.Series):
        static_covariates (pd.DataFrame): time independent  covariates. numeric only dataframe

    """
    non_numeric_cols = utils.non_numeric_columns(static_covariates)
    if non_numeric_cols:
        msg = """

        Input dataframe contains non numeric columns: {}.
        Please convert text columns using `rpy_utils.to_categorical` method first""".format(non_numeric_cols)
        raise NonNumericCovariateError(msg)

    if isinstance(ftime, pd.Series):
        ftime = ftime.values
    r_ftime = rpy_utils.r_vector(ftime)

    if isinstance(fstatus, pd.Series):
        fstatus = fstatus.values
    r_fstatus = rpy_utils.r_vector(fstatus)

    r_static_cov = rpy_utils.r_dataframe(static_covariates)

    if cengroup is not None:
        r_cengroup = rpy_utils.r_vector(cengroup)
        kwargs['cengroup'] = r_cengroup

    if subset is not None:
        r_subset = rpy_utils.r_vector(subset)
        kwargs['subset'] = r_subset

    r_crr_result = r_cmprsk.crr(r_ftime, r_fstatus, r_static_cov,
                                failcode=failcode, cencode=cencode, **kwargs)
    return CrrResult(r_crr_result)
