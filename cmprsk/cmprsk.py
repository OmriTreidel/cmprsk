import numpy as np
import pandas as pd

from collections import namedtuple
from rpy2.robjects import pandas2ri, numpy2ri
from rpy2.robjects.packages import importr as import_R
from scipy.stats import norm as normal

from . import rpy_utils
from . import utils

numpy2ri.activate()


r_cmprsk = import_R('cmprsk')


class NonNumericCovariateError(Exception):
    pass


class CrrResult(object):
    """An parser for the result coming from crr.

    The full result is accessible via CrrResult.raw
    """
    def __init__(self, r_crr_res):
        self.raw = r_crr_res
        self.parsed = self.asdict()
        self._coefficients = self.parsed['coef']
        self._names = list(self.raw[0].names)
        self._covariance = self.parsed['var']
        self._std = np.sqrt(np.diag(self._covariance))

    def asdict(self):
        return rpy_utils.parse_r_list(self.raw)

    @property
    def names(self):
        return self._names

    @property
    def coefficients(self):
        return self._coefficients

    @property
    def std(self):
        return self._std

    @property
    def covariance(self):
        return self._covariance

    @property
    def p_values(self):
        _p_vals = [p_value(beta, std) for beta, std in
                    zip(self.coefficients, self.std)]
        return np.array(_p_vals)

    def hazard_ratio(self, conf_level=0.95):
        values = np.zeros(len(self.coefficients))
        confidence = np.zeros((len(self.coefficients), 2))
        edges = np.array(normal.interval(conf_level))
        for i, (coef, std) in enumerate(zip(self.coefficients, self.std)):
            values[i] = np.exp(coef)
            confidence[i, :] = [np.exp(coef + edges[0] * std),
                                np.exp(coef + edges[1] * std)]
        return values, confidence

    @property
    def summary(self):
        cols = ['names', 'coefficients', 'std', 'hazard_ratio',
                'hazard_ratio_2.5%', 'hazard_ratio_97.5%', 'p_values']
        out = pd.DataFrame(columns=cols)
        out['coefficients'] = self.coefficients
        out['std'] = self.std
        hazard_ratio, confidence = self.hazard_ratio()
        out['hazard_ratio'] = hazard_ratio
        out[['hazard_ratio_2.5%', 'hazard_ratio_97.5%']] = confidence
        out['p_values'] = self.p_values
        out['names'] = self.names
        return out.set_index('names')


def p_value(x, std):
    return 2 * (1 - normal.cdf(abs(x/std)))


def crr(failure_time, failure_status, static_covariates, cengroup=None, failcode=1, cencode=0,
        subset=None, **kwargs):
    """
    Args:
        failure_time (np.array or pandas.Series): vector of failure/censoring times
        failure_status (np.array or pandas.Series): vector with a unique code for each failure type and a separate
            code for censored observations
        static_covariates (pd.DataFrame): time independent  covariates. numeric only dataframe

    Keyword Args:
        cengroup (np.array ofpandas.Series): vector with different values for
            each group with a distinct censoring distribution
        failcode (int): code of fstatus that denotes the failure type of interest
        cencode (int): code of fstatus that denotes censored observations
        subset (numpy.array or pandas Series): a logical vector specifying a subset of cases
            to include in the analysis

    Note:
        na.action is `omit`

    Returns:
        CrrResult: a wrapper around crr_result
    """
    non_numeric_cols = utils.non_numeric_columns(static_covariates)
    if non_numeric_cols:
        msg = """

        Input dataframe contains non numeric columns: {}.
        Please convert text columns using `rpy_utils.to_categorical` method first""".format(non_numeric_cols)
        raise NonNumericCovariateError(msg)

    if isinstance(failure_time, pd.Series):
        failure_time = failure_time.values
    r_ftime = rpy_utils.r_vector(failure_time)

    if isinstance(failure_status, pd.Series):
        failure_status = failure_status.values
    r_fstatus = rpy_utils.r_vector(failure_status)

    r_static_cov = rpy_utils.r_dataframe(static_covariates)

    if cengroup is not None:
        r_cengroup = rpy_utils.r_vector(cengroup)
        kwargs['cengroup'] = r_cengroup

    if subset is not None:
        if isinstance(subset, pd.Series):
            subset = subset.values
        r_subset = rpy_utils.r_vector(subset)
        kwargs['subset'] = r_subset

    r_crr_result = r_cmprsk.crr(r_ftime, r_fstatus, r_static_cov,
                                failcode=failcode, cencode=cencode, **kwargs)
    return CrrResult(r_crr_result)


def cuminc(failure_time, failure_status, group=None, strata=None, rho=0, cencode=0, subset=None,
           **kwargs):
    """
    Args:
        failure_time (numpy.array or pandas.Series): failure time variable
        failure_status (numpy.array or pandas.Series): variable with distinct codes
            for different causes of failure and also a distinct code for censored observations

    Keyword Args:
        group (numpy.array or pandas.Series): estimates will calculated within groups given by
            distinct values of this variable. Tests will compare these groups. If missing then
            treated as all one group (no test statistics)
        strata (numpy.array or pandas.Series): stratification variable. Has no effect on estimates.
            Tests will be stratified on this variable. (all data in 1 stratum, if missing)
        rho (int): Power of the weight function used in the tests.
        cencode (int): value of fstatus variable which indicates the failure time is censored
        subset (numpy.array or pandas.Series): a logical vector specifying a subset of cases
            to include in the analysis

    Returns:
        CumincResult: a wrapper around the result.

    Note:
        na.action is `omit`
    """
    if isinstance(failure_time, pd.Series):
        failure_time = failure_time.values
    r_ftime = rpy_utils.r_vector(failure_time)

    if isinstance(failure_status, pd.Series):
        failure_status = failure_status.values
    r_fstatus = rpy_utils.r_vector(failure_status)

    if group is not None:
        if isinstance(group, pd.Series):
            group = group.values
        r_group = rpy_utils.r_vector(group)
        kwargs['group'] = r_group

    if strata is not None:
        if isinstance(strata, pd.Series):
            strata = strata.values
        r_strata = rpy_utils.r_vector(strata)
        kwargs['strata'] = r_strata

    if subset is not None:
        if isinstance(subset, pd.Series):
            subset = subset.values
        r_subset = rpy_utils.r_vector(subset)
        kwargs['subset'] = r_subset

    cuminc_res = r_cmprsk.cuminc(failure_time, failure_status,
                                 rho=rho, cencode=cencode, **kwargs)
    return CumincResult(cuminc_res, stats=(group is not None))


class CumincGroup(object):

    def __init__(self, time, est, var):
        self.time = time
        self.est = est
        self.var =  var
        self.std = np.sqrt(self.var)

    @property
    def low_ci(self):
        return self.est - 2 * self.std

    @property
    def high_ci(self):
        return self.est + 2 * self.std


class CumincResult(object):
    """An parser for the result coming from crr.

    The raw result is accessible via CumincResult.raw

    To get the summary use `print` property

    In order to plot use the `groups` member - see Example in the README.

    Note:
        groups is a dictionary with keys that are the group name (e.g `1 2`)
        and the values are `CumincGroup` i.e. they have members: time, est, var and
        low_ci, high_ci properties.
    """
    def __init__(self, r_cuminc_res, stats=None):
        print('stats: ', stats)
        self.raw = r_cuminc_res
        self._stats = self.parse_stats() if stats else None
        self._set_groups()

    def parse_stats(self):
        r_stats = self.raw[-1]
        return pd.DataFrame(pandas2ri.ri2py(r_stats), columns=r_stats.colnames)

    @property
    def stats(self):
        return self._stats

    def _set_groups(self):
        self.groups = dict()
        if self._stats is not None:
            for group, name in zip(self.raw[:-1], self.raw.names[:-1]):
                self.groups[name] = CumincGroup(*[np.array(element) for element in group])
        else:
            for group, name in zip(self.raw, self.raw.names):
                self.groups[name] = CumincGroup(*[np.array(element) for element in group])
    @property
    def print(self):
        print(self.raw)
