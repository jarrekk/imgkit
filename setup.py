# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools.command.test import test
import os
import sys
import imgkit


class PyTest(test):
    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = ['imgkit-tests.py']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        os.chdir('tests/')
        err_no = pytest.main(self.test_args)
        sys.exit(err_no)


def long_description():
    try:
        import pypandoc
        long_desc = pypandoc.convert_file('README.md', 'rst')
        long_desc += '\n' + pypandoc.convert_file('HISTORY.md', 'rst')
        long_desc += '\n' + pypandoc.convert_file('AUTHORS.md', 'rst')
    except(IOError, ImportError):
        long_desc = open('README.md').read()
        long_desc += '\n' + open('HISTORY.md').read()
        long_desc += '\n' + open('AUTHORS.md').read()
    return long_desc


setup(
    name='imgkit',
    version=imgkit.__version__,
    description=imgkit.__doc__.strip(),
    # push to pypi should use this
    long_description=imgkit.__doc__.strip(),
    # long_description=long_description(),
    download_url='https://github.com/jarrekk/imgkit',
    license=imgkit.__license__,
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    packages=['imgkit'],
    author=imgkit.__author__,
    author_email=imgkit.__contact__,
    url=imgkit.__homepage__,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Utilities'
    ]
)
