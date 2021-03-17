# -*- coding: utf-8 -*-
import subprocess
from subprocess import CalledProcessError


class Config(object):
    def __init__(self, wkhtmltoimage='', xvfb='', meta_tag_prefix='imgkit-'):
        """
        :param wkhtmltoimage: wkhtmltoimage path
        :param xvfb: xvfb path
        :param meta_tag_prefix: the prefix for `imgkit` specific meta tags - by default this is `imgkit-`
        """
        self.wkhtmltoimage = wkhtmltoimage
        self.xvfb = xvfb
        self.meta_tag_prefix = meta_tag_prefix

        if not self.wkhtmltoimage:
            # get wkhtmltoimage in *nix/windows server
            # see https://github.com/jarrekk/imgkit/issues/57 for windows condition
            for find_cmd in ('where', 'which'):
                try:
                    self.wkhtmltoimage = subprocess.check_output([find_cmd, 'wkhtmltoimage']).strip()
                    break
                except CalledProcessError:
                    self.wkhtmltoimage = ''
                except OSError:
                    self.wkhtmltoimage = ''

        if not self.xvfb:
            # get xvfb in *nix/windows server
            # see https://github.com/jarrekk/imgkit/issues/57 for windows condition
            for find_cmd in ('where', 'which'):
                try:
                    self.xvfb = subprocess.check_output([find_cmd, 'xvfb-run']).strip()
                    break
                except CalledProcessError:
                    self.xvfb = ''
                except OSError:
                    self.xvfb = ''

        try:
            with open(self.wkhtmltoimage):
                pass
        except IOError:
            raise IOError('No wkhtmltoimage executable found: "{0}"\n'
                          'If this file exists please check that this process can '
                          'read it. Otherwise please install wkhtmltopdf - '
                          'http://wkhtmltopdf.org\n'.format(self.wkhtmltoimage))
        if self.xvfb:
            try:
                with open(self.xvfb):
                    pass
            except IOError:
                raise IOError('No xvfb executable found: "{0}"\n'
                              'If this file exists please check that this process can '
                              'read it. Otherwise please install xvfb -'.format(self.xvfb))
