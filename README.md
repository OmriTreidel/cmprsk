# cmprsk
Regression modeling of sub-distribution functions in competing risks

A python wrapper around the [cmprsk](https://cran.r-project.org/web/packages/cmprsk/index.html) R package.

### How to update package:
0. update version in setup.py
1. rm -fr dist directory
2. python setup.py sdist bdist_wheel 
3. twine upload  dist/* --verbose
