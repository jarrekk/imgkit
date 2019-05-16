# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools.command.test import test
import os
import sys
import imgkit


class PyTest(test):
    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = ['imgkit_test.py']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        os.chdir('test/')
        err_no = pytest.main(self.test_args)
        sys.exit(err_no)


def long_description():
    try:
        import pypandoc
        long_desc = pypandoc.convert_file('README.md', 'rst')
        long_desc += '\n' + pypandoc.convert_file('AUTHORS.md', 'rst')
    except Exception as e:
        print(e)
        long_desc = imgkit.__doc__.strip()
    return long_desc


setup(
    name='imgkit',
    version=imgkit.__version__,
    description=imgkit.__doc__.strip(),
    long_description=long_description(),
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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Utilities'
    ]
)
