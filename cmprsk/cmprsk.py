from rpy2.robjects.packages import importr as import_R

from . import rpy_utils
from . import utils


cmprsk = import_R('cmprsk')


class CrrResult(object):
    def __init__(self, r_crr_res):
        self.raw = r_crr_res
        # TODO: finish parsing

    def summary(self):
        print(self.raw)


def crr(ftime, fstatus, covariates_1):
    """
    Args:
        ftime (np.array):
        fstatus (np.array):
        covariates_1 (pd.DataFrame): numeric only dataframe
        # covariates_2 (pd.DataFrame): numeric only dataframe
    """
    non_numeric_cols = utils.non_numeric_columns(covariates_1)
    if non_numeric_cols:
        msg = """

        Input dataframe contains non numeric columns: {}.
        Please convert text columns using `rpy_utils.to_categorical` method first""".format(non_numeric_cols)
        raise InputError(msg)

    r_cov_1 = rpy_utils.r_dataframe(covariates_1)
    r_ftime = r_vector(ftime)
    r_fstatus = r_vector(fstatus)
    r_crr_result = cmprsk.crr(r_ftime, r_fstatus, r_cov_1)
    return CrrResult(r_crr_result)
