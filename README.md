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

### How to update package:
0. update version in setup.py
1. rm -fr dist directory
2. python setup.py sdist bdist_wheel 
3. twine upload  dist/* --verbose
