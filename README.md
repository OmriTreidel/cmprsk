# cmprsk - Competing Risks Regression
Regression modeling of sub-distribution functions in competing risks.

A python wrapper around the [cmprsk](https://cran.r-project.org/web/packages/cmprsk/index.html) R package.

*Description*: Estimation, testing and regression modeling of
subdistribution functions in competing risks, as described in Gray
(1988), A class of K-sample tests for comparing the cumulative
incidence of a competing risk, **Ann. Stat. 16:1141-1154, and Fine JP and
Gray RJ (1999), A proportional hazards model for the subdistribution
of a competing risk, JASA, 94:496-509**.

[Original Package documentation](https://cran.r-project.org/web/packages/cmprsk/cmprsk.pdf)

## Requirements

### python
* Only python 3 is now supported. Recommended python version >= 3.8 

###
* The original version of this package was written with `rpy2` version 2.9.4. Since then, `rpy2` had many breaking changes. 
Therefore `cmprsk` version **0.X.Y** only works with `rpy2` version 2.9.X.
* The `cmprsk` package v **1.X.Y** is now up-to-date and is using `rpy2` 3.4.5. 

### Installation steps

* install `R`
* install `cmprsk` R package: open R terminal and run `install.packages("cmprsk")`
* create a virtual environment (recommended)
* install`rpy2` - if using `conda` for creating the virtual environment on MacOS M1 (apple silicon) install `rpy2` using pip (tested on version 3.5.9) 
* install `pandas` (tested on version 1.5.3)
* install `scipy` (tested on version 1.10.1)
* install `pytest` and `pytest-cov` for running unit tests (dev) only

This package is using `rpy2` in order to use import the cmprsk R packge and therefore the [requirements for rpy2](https://rpy2.readthedocs.io/en/version_2.8.x/overview.html?highlight=readline#requirements) must be met.

TL;DR
* Unix like OS: Linux, MacOS, BSD. (May work on Windows, look at [rpy2 binaries])(https://rpy2.readthedocs.io/en/version_2.8.x/overview.html#microsoft-s-windows-precompiled-binaries). 
* python >= 3.5
* R >= 3.3 [how to install R](https://www.datacamp.com/community/tutorials/installing-R-windows-mac-ubuntu)
* readline 7.0 - Should be installed as part of `rpy2`. [how to install on MacOS](http://blogs.perl.org/users/aristotle/2013/07/easy-osx-termreadlinegnu.html) see also the following [issue](https://github.com/conda-forge/rpy2-feedstock/issues/1)
* The`cmprsk` R library (open the R consule and run `install.packages('cmprsk')`)

## Quickstart

For example usage consult the tutorial notebook in this repo: `package_usage.ipynb`

### Example: crr

```python

import pandas as pd

import cmprsk.cmprsk as cmprsk

from cmprsk import utils

data = pd.read_csv('my_data_file.csv')
# assuming that x1,x2,x3, x4 are covatiates. 
# x1 are x4 are categorical with baseline 'd' for x1 and 5 for x2 
static_covariates = utils.as_indicators(data[['x1', 'x2', 'x3', 'x4']], ['x1', 'x4'], bases=['d', 5])

crr_result = cmprsk.crr(data['ftime'], data['fstatus'], static_covariates)
report = crr_result.summary

print(report)

```
`ftime` and `fstatus` can be numpy array or pandas series, and `static_covariates` is a pandas DataFrame.
The `report` is a pandas `DataFrame` as well. 

### Example: cuminc

```python
import matplotlib.plt
import numpy as np
import pandas as pd


from cmprsk import cmprsk

data  = pd.read_csv('cmprsk/cmprsk/tests/example_dataset.csv')
cuminc_res = cmprsk.cuminc(data.ss, data.cc, group=data.gg, strata=data.strt)

# print
cuminc_res.print

# plot using matplotlib

_, ax = plt.subplots()
for name, group in cuminc_res.groups.items():
    ax.plot(group.time, group.est, label=name)
    ax.fill_between(group.time, group.low_ci, group.high_ci, alpha=0.4)
    
ax.set_ylim([0, 1])
ax.legend()
ax.set_title('foo bar')
plt.show()

```
## Development
For running the unit tests run 

    pytest --cov=cmprsk cmprsk/tests/

from the project root. Note: you'll need to install [pytest-cov](https://pypi.org/project/pytest-cov/).

Current coverage
```buildoutcfg
---------- coverage: platform darwin, python 3.9.7-final-0 -----------
Name                             Stmts   Miss  Cover
----------------------------------------------------
cmprsk/__init__.py                   0      0   100%
cmprsk/cmprsk.py                   128     22    83%
cmprsk/rpy_utils.py                 44     10    77%
cmprsk/tests/__init__.py             0      0   100%
cmprsk/tests/test_cmprsk.py         30      0   100%
cmprsk/tests/test_rpy_utils.py      27      1    96%
cmprsk/tests/test_utils.py          37      0   100%
cmprsk/utils.py                     23      1    96%
----------------------------------------------------
TOTAL                              289     34    88%
```

### How to update package:
0. update version in setup.py
1. rm -fr dist directory
2. python setup.py sdist bdist_wheel 
3. twine upload  dist/* --verbose
