"""
Justice client library.
"""
import os
import re

try:
    import setuptools
except ImportError:
    import distutils.core
    setup = distutils.core.setup
else:
    setup = setuptools.setup


def _get_version():
    path = os.path.join(PATH_TO_FILE, 'justice_client.py')
    version_re = r".*__version__ = '(.*?)'"
    fo = open(path)
    try:
        return re.compile(version_re, re.S).match(fo.read()).group(1)
    finally:
        fo.close()


def _get_long_description():
    path = os.path.join(PATH_TO_FILE, 'README.rst')
    fo = open(path)
    try:
        return fo.read()
    finally:
        fo.close()


PATH_TO_FILE = os.path.dirname(__file__)
VERSION = _get_version()
LONG_DESCRIPTION = _get_long_description()

setup(
    name='justice',
    version=VERSION,
    url='https://www.balancedpayments.com/',
    license='BSD',
    author='No One',
    author_email='justice@balancedpayments.com',
    description='Justice client library',
    long_description=LONG_DESCRIPTION,
    tests_require=[
        'nose==1.1.2',
        'mock==0.8',
    ],
    install_requires=[
        'iso8601 ==0.1.4',
        'simplejson ==2.3.2',
        'wac >=0.11',
    ],
    test_suite='nose.collector',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
