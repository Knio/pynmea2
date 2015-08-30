from setuptools import setup

import imp
_version = imp.load_source("pynmea2._version", "pynmea2/_version.py")

setup(
    name='pynmea2',
    version=_version.__version__,
    author='Tom Flanagan',
    author_email='tom@zkpq.ca',
    license='MIT',
    url='https://github.com/Knio/pynmea2',

    description='Python library for the NMEA 0183 protcol',
    packages=['pynmea2','pynmea2.types','pynmea2.types.proprietary'],
    keywords='python nmea gps parse parsing nmea0183 0183',

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
