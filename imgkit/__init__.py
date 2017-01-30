# -*- coding: utf-8 -*-
"""
Wkhtmltopdf python wrapper to convert html to image using the webkit rendering engine and qt
"""

__author__ = 'JiaKunUp'
__version__ = '0.0.2'
__license__ = 'MIT'

from .imgkit import IMGKit
from .api import from_url, from_file, from_string, config
