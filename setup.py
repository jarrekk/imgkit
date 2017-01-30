# -*- coding: utf-8 -*-
import codecs
from distutils.core import setup
from setuptools.command.test import test
import re
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
    """Pre-process the README so that PyPi can render it properly."""
    with codecs.open('README.md', encoding='utf8') as f:
        rst = f.read()
    code_block = '(:\n\n)?\.\. code-block::.*'
    rst = re.sub(code_block, '::', rst)
    return rst + '\n\n' + open('HISTORY.md').read()


setup(
    name='imgkit',
    version=imgkit.__version__,
    description=imgkit.__doc__.strip(),
    long_description=long_description(),
    download_url='https://github.com/JiaKunUp/imgkit',
    license=imgkit.__license__,
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    packages=['imgkit'],
    author=imgkit.__author__,
    author_email='me@jack003.com',
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
