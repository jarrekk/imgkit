# -*- coding: utf-8 -*-
"""
Wkhtmltopdf python wrapper to convert html to image using the webkit rendering engine and qt
"""

__author__ = 'jarrekk'
__contact__ = 'me@jack003.com'
__version__ = '0.1.2'
__homepage__ = 'http://github.com/jarrekk/imgkit'
__license__ = 'MIT'

from .imgkit import IMGKit
from .api import from_url, from_file, from_string, config
