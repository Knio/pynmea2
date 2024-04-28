import importlib.machinery
import importlib.util

from setuptools import setup


def load_source(modname, filename):
    """Load a source file and return its module object.

    From: https://docs.python.org/3.12/whatsnew/3.12.html#imp
    """
    loader = importlib.machinery.SourceFileLoader(modname, filename)
    spec = importlib.util.spec_from_file_location(modname, filename, loader=loader)
    module = importlib.util.module_from_spec(spec)
    # The module is always executed and not cached in sys.modules.
    # Uncomment the following line to cache the module.
    # sys.modules[module.__name__] = module
    loader.exec_module(module)
    return module

_version = load_source("pynmea2._version", "pynmea2/_version.py")

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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
