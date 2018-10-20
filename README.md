# cmprsk
Regression modeling of sub-distribution functions in competing risks.

A python wrapper around the [cmprsk](https://cran.r-project.org/web/packages/cmprsk/index.html) R package.

*Description*: Estimation, testing and regression modeling of
subdistribution functions in competing risks, as described in Gray
(1988), A class of K-sample tests for comparing the cumulative
incidence of a competing risk, **Ann. Stat. 16:1141-1154, and Fine JP and
Gray RJ (1999), A proportional hazards model for the subdistribution
of a competing risk, JASA, 94:496-509**.

[Original Package documentation](https://cran.r-project.org/web/packages/cmprsk/cmprsk.pdf)

## Requierments
This package is using `rpy2` in order to use import the cmprsk R packge and therefore the [requierments for rpy2](https://rpy2.readthedocs.io/en/version_2.8.x/overview.html?highlight=readline#requirements) must be met.

TL;DR
* Unix like OS: Linux, MacOS, BSD. May work on Windows, look at [rpy2 binaries](https://rpy2.readthedocs.io/en/version_2.8.x/overview.html#microsoft-s-windows-precompiled-binaries). 
* python >= 3.5
* R > 3.2 [install R](https://www.datacamp.com/community/tutorials/installing-R-windows-mac-ubuntu)
* readline 7.0 [install on MacOS](http://blogs.perl.org/users/aristotle/2013/07/easy-osx-termreadlinegnu.html) see also the following [issue](https://github.com/conda-forge/rpy2-feedstock/issues/1)

## Quickstart

```python

import pandas as pd

import cmprsk.cmprsk as cmprsk

from cmprsk import utils

data = pd.read_csv('my_data_fle')
# assuming that x1,x2,x3, x4 are covatiates. 
# x1 are x4 are categorical with baseline 'd' for x1 and 5 for x2 
static_covariates = utils.as_indicators(data[['x1', 'x2', 'x3', 'x4']], ['x1', 'x4'], bases=['d', 5])

crr_result = cmprsk.crr(ftime, fstatus, static_covariates)
report = crr_result.summary

print(report)

```
`ftime` and `fstatus` can be numpy array or pandas series, and `static_covariates` is a pandas DataFrame.
The `report` is a pandas `DataFrame` as well. 


### How to update package:
0. update version in setup.py
1. rm -fr dist directory
2. python setup.py sdist bdist_wheel 
3. twine upload  dist/* --verbose
