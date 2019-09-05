# -*- coding: utf-8 -*-
import shutil


class Config(object):
    def __init__(self, wkhtmltoimage='', meta_tag_prefix='imgkit-'):
        self.meta_tag_prefix = meta_tag_prefix

        self.wkhtmltoimage = wkhtmltoimage

        self.xvfb = ''

        if not self.wkhtmltoimage:
            self.wkhtmltoimage = shutil.which("wkhtmltoimage")

        if not self.xvfb:
            self.xvfb = shutil.which("xvfb-run")

        if not self.wkhtmltoimage:
            raise IOError('No wkhtmltoimage executable found: "{0}"\n'
                          'If this file exists please check that this process can '
                          'read it. Otherwise please install wkhtmltopdf - '
                          'http://wkhtmltopdf.org\n'.format(self.wkhtmltoimage))

        if not self.xvfb:
            raise IOError('No xvfb-run executable found: "{0}"\n'
                          'If this file exists please check that this process can '
                          'read it. Otherwise please install xvfb-run'.format(self.xvfb))
