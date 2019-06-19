from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import os
import sys


here = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='dollar-tracker',
    version='1.0.0.dev1',
    url='https://github.com/mscaceres/dollar-tracker',
    license='',
    author='Mauro Caceres',
    tests_require=['pytest'],
    install_requires=[
        'beautifulsoup4==4.4.1',
        'plotly==1.9.6',
        'docopt==0.6.2',
        'prompt-toolkit==2.0.9'
    ],
    cmdclass={'test': PyTest},
    author_email='mauro.caceres@gmail.com',
    description='review the dollar price history from many sources in a consolidated graphic',
    long_description='',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    test_suite='',
    classifiers=[
    ],
    extras_require={
        'testing': ['pytest'],
    },
    entry_points= {
        'console_scripts': ['dollar-tracker=dollar_tracker.main:main']
    }
)
