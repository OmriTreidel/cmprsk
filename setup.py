import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cmprsk",
    version="1.0.0",
    author="Omri Treidel",
    author_email="treidel2@gmail.com",
    description="A python wrapper around cmprsk R package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OmriTreidel/cmprsk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'numpy',
          'pandas',
          'rpy2',
          'scipy',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    keywords=[
    'competing risks',
    'survival analysis',
    ],
)
