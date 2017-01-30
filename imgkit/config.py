# -*- coding: utf-8 -*-
import subprocess
import sys


class Config(object):
    def __init__(self, wkhtmltoimage='', meta_tag_prefix='imgkit-'):
        self.meta_tag_prefix = meta_tag_prefix

        self.wkhtmltoimage = wkhtmltoimage

        if not self.wkhtmltoimage:
            if sys.platform == 'win32':
                self.wkhtmltoimage = subprocess.Popen(['where', 'wkhtmltoimage'],
                                                      stdout=subprocess.PIPE).communicate()[0].strip()
            else:
                self.wkhtmltoimage = subprocess.Popen(['which', 'wkhtmltoimage'],
                                                      stdout=subprocess.PIPE).communicate()[0].strip()

        try:
            with open(self.wkhtmltoimage) as f:
                pass
        except IOError:
            raise IOError('No wkhtmltoimage executable found: "%s"\n'
                          'If this file exists please check that this process can '
                          'read it. Otherwise please install wkhtmltopdf - '
                          'http://wkhtmltopdf.org' % self.wkhtmltoimage)
