# -*- coding: utf-8 -*-
import os
import io
import sys
import codecs
import unittest

# Prepend ../ to PYTHONPATH so that we can import IMGKIT form there.
TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.realpath(os.path.join(TESTS_ROOT, '..')))

import imgkit


class TestIMGKitInitialization(unittest.TestCase):
    """Test init"""

    def test_html_source(self):
        r = imgkit.IMGKit('<h1>Oh hai</h1>', 'string')
        self.assertTrue(r.source.isString())

    def test_url_source(self):
        r = imgkit.IMGKit('http://ya.ru', 'url')
        self.assertTrue(r.source.isUrl())

    def test_file_source(self):
        r = imgkit.IMGKit('test/fixtures/example.html', 'file')
        self.assertTrue(r.source.isFile())

    def test_file_object_source(self):
        with open('test/fixtures/example.html') as fl:
            r = imgkit.IMGKit(fl, 'file')
            self.assertTrue(r.source.isFileObj())

    def test_file_source_with_path(self):
        r = imgkit.IMGKit('test', 'string')
        with io.open('test/fixtures/example.css') as f:
            self.assertTrue(r.source.isFile(path=f))
        with codecs.open('test/fixtures/example.css', encoding='UTF-8') as f:
            self.assertTrue(r.source.isFile(path=f))

    def test_options_parsing(self):
        r = imgkit.IMGKit('html', 'string', options={'format': 'jpg'})
        test_command = r.command('test')
        idx = test_command.index('--format')  # Raise exception in case of not found
        self.assertTrue(test_command[idx + 1] == 'jpg')

    def test_options_parsing_with_dashes(self):
        r = imgkit.IMGKit('html', 'string', options={'--format': 'jpg'})

        test_command = r.command('test')
        idx = test_command.index('--format')  # Raise exception in case of not found
        self.assertTrue(test_command[idx + 1] == 'jpg')

    def test_options_parsing_with_tuple(self):
        options = {
            '--custom-header': [
                ('Accept-Encoding', 'gzip')
            ]
        }
        r = imgkit.IMGKit('html', 'string', options=options)
        command = r.command()
        idx1 = command.index('--custom-header')  # Raise exception in case of not found
        self.assertTrue(command[idx1 + 1] == 'Accept-Encoding')
        self.assertTrue(command[idx1 + 2] == 'gzip')

    def test_options_parsing_with_tuple_no_dashes(self):
        options = {
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ]
        }
        r = imgkit.IMGKit('html', 'string', options=options)
        command = r.command()
        idx1 = command.index('--custom-header')  # Raise exception in case of not found
        self.assertTrue(command[idx1 + 1] == 'Accept-Encoding')
        self.assertTrue(command[idx1 + 2] == 'gzip')

    def test_repeatable_options(self):
        roptions = {
            '--format': 'jpg',
            'cookies': [
                ('test_cookie1', 'cookie_value1'),
                ('test_cookie2', 'cookie_value2'),
            ]
        }

        r = imgkit.IMGKit('html', 'string', options=roptions)

        test_command = r.command('test')

        idx1 = test_command.index('--format')  # Raise exception in case of not found
        self.assertTrue(test_command[idx1 + 1] == 'jpg')

        self.assertTrue(test_command.count('--cookies') == 2)

        idx2 = test_command.index('--cookies')
        self.assertTrue(test_command[idx2 + 1] == 'test_cookie1')
        self.assertTrue(test_command[idx2 + 2] == 'cookie_value1')

        idx3 = test_command.index('--cookies', idx2 + 2)
        self.assertTrue(test_command[idx3 + 1] == 'test_cookie2')
        self.assertTrue(test_command[idx3 + 2] == 'cookie_value2')

    def test_custom_config(self):
        conf = imgkit.config()
        self.assertEqual('imgkit-', conf.meta_tag_prefix)
        conf = imgkit.config(meta_tag_prefix='prefix-')
        self.assertEqual('prefix-', conf.meta_tag_prefix)
        with self.assertRaises(IOError):
            imgkit.config(wkhtmltoimage='wrongpath')


class TestIMGKitCommandGeneration(unittest.TestCase):
    """Test command() method"""

    def test_command_construction(self):
        r = imgkit.IMGKit('html', 'string', options={'format': 'jpg', 'toc-l1-font-size': 12})
        command = r.command()
        self.assertEqual(command[0], r.wkhtmltoimage)
        self.assertEqual(command[command.index('--format') + 1], 'jpg')
        self.assertEqual(command[command.index('--toc-l1-font-size') + 1], '12')

    def test_lists_of_input_args(self):
        urls = ['http://ya.ru', 'http://google.com']
        paths = ['test/fixtures/example.html', 'test/fixtures/example.html']
        r = imgkit.IMGKit(urls, 'url')
        r2 = imgkit.IMGKit(paths, 'file')
        cmd = r.command()
        cmd2 = r2.command()
        self.assertEqual(cmd[-3:], ['http://ya.ru', 'http://google.com', '-'])
        self.assertEqual(cmd2[-3:], ['test/fixtures/example.html', 'test/fixtures/example.html', '-'])

    def test_read_source_from_stdin(self):
        r = imgkit.IMGKit('html', 'string')
        self.assertEqual(r.command()[-2:], ['-', '-'])

    def test_url_in_command(self):
        r = imgkit.IMGKit('http://ya.ru', 'url')
        self.assertEqual(r.command()[-2:], ['http://ya.ru', '-'])

    def test_file_path_in_command(self):
        path = 'test/fixtures/example.html'
        r = imgkit.IMGKit(path, 'file')
        self.assertEqual(r.command()[-2:], [path, '-'])

    def test_output_path(self):
        out = '/test/test2/out.jpg'
        r = imgkit.IMGKit('html', 'string')
        self.assertEqual(r.command(out)[-1:], ['/test/test2/out.jpg'])

    def test_imgkit_meta_tags(self):
        body = """
        <html>
          <head>
            <meta name="imgkit-format" content="jpg"/>
            <meta name="imgkit-orientation" content="Landscape"/>
          </head>
        """

        r = imgkit.IMGKit(body, 'string')
        command = r.command()
        self.assertEqual(command[command.index('--format') + 1], 'jpg')
        self.assertEqual(command[command.index('--orientation') + 1], 'Landscape')

    def test_imgkit_meta_tags_in_bad_markup(self):
        body = """
        <html>
          <head>
            <meta name="imgkit-format" content="jpg"/>
            <meta name="imgkit-orientation" content="Landscape"/>
          </head>
          <br>
        </html>
        """

        r = imgkit.IMGKit(body, 'string')
        command = r.command()
        self.assertEqual(command[command.index('--format') + 1], 'jpg')
        self.assertEqual(command[command.index('--orientation') + 1], 'Landscape')

    def test_skip_nonimgkit_tags(self):
        body = """
        <html>
          <head>
            <meta name="test-page-size" content="Legal"/>
            <meta name="imgkit-orientation" content="Landscape"/>
          </head>
          <br>
        </html>
        """

        r = imgkit.IMGKit(body, 'string')
        command = r.command()
        self.assertEqual(command[command.index('--orientation') + 1], 'Landscape')

    def test_toc_handling_without_options(self):
        r = imgkit.IMGKit('hmtl', 'string', toc={'xsl-style-sheet': 'test.xsl'})
        self.assertEqual(r.command()[1], 'toc')
        self.assertEqual(r.command()[2], '--xsl-style-sheet')

    def test_toc_with_options(self):
        options = {
            'format': 'jpg',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8"
        }
        r = imgkit.IMGKit('html', 'string', options=options, toc={'xsl-style-sheet': 'test.xsl'})

        command = r.command()

        self.assertEqual(command[1 + len(options) * 2], 'toc')
        self.assertEqual(command[1 + len(options) * 2 + 1], '--xsl-style-sheet')

    def test_cover_without_options(self):
        r = imgkit.IMGKit('html', 'string', cover='test.html')

        command = r.command()

        self.assertEqual(command[1], 'cover')
        self.assertEqual(command[2], 'test.html')

    def test_cover_with_options(self):
        options = {
            'format': 'jpg',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8"
        }
        r = imgkit.IMGKit('html', 'string', options=options, cover='test.html')

        command = r.command()

        self.assertEqual(command[1 + len(options) * 2], 'cover')
        self.assertEqual(command[1 + len(options) * 2 + 1], 'test.html')

    def test_cover_and_toc(self):
        options = {
            'format': 'jpg',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8"
        }
        r = imgkit.IMGKit('html', 'string', options=options, toc={'xsl-style-sheet': 'test.xsl'}, cover='test.html')
        command = r.command()
        self.assertEqual(command[-7:], ['toc', '--xsl-style-sheet', 'test.xsl', 'cover', 'test.html', '-', '-'])

    def test_cover_and_toc_cover_first(self):
        options = {
            'format': 'jpg',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8"
        }
        r = imgkit.IMGKit('html', 'string', options=options, toc={'xsl-style-sheet': 'test.xsl'}, cover='test.html',
                          cover_first=True)
        command = r.command()
        self.assertEqual(command[-7:], ['cover', 'test.html', 'toc', '--xsl-style-sheet', 'test.xsl', '-', '-'])

    def test_outline_options(self):
        options = {
            'outline': None,
            'outline-depth': 1
        }

        r = imgkit.IMGKit('ya.ru', 'url', options=options)
        cmd = r.command()
        # self.assertEqual(cmd[1:], ['--outline', '--outline-depth', '1', 'ya.ru', '-'])
        self.assertIn('--outline', cmd)
        self.assertEqual(cmd[cmd.index('--outline-depth') + 1], '1')

    def test_filter_empty_and_none_values_in_opts(self):
        options = {
            'outline': '',
            'footer-line': None,
            'quiet': False
        }

        r = imgkit.IMGKit('html', 'string', options=options)
        cmd = r.command()
        self.assertEqual(len(cmd), 6)


class TestIMGKitGeneration(unittest.TestCase):
    """Test to_img() method"""

    def setUp(self):
        pass

    def tearDown(self):
        if os.path.exists('out.jpg'):
            os.remove('out.jpg')

    def test_img_generation(self):
        r = imgkit.IMGKit('html', 'string', options={'format': 'jpg'})
        pic = r.to_img('out.jpg')
        self.assertTrue(pic)

    def test_img_generation_xvfb(self):
        r = imgkit.IMGKit('html', 'string', options={'format': 'jpg', 'xvfb': ''})
        pic = r.to_img('out.jpg')
        self.assertTrue(pic)

    def test_raise_error_with_invalid_url(self):
        r = imgkit.IMGKit('wrongurl', 'url')
        with self.assertRaises(IOError):
            r.to_img('out.jpg')

    def test_raise_error_with_invalid_file_path(self):
        paths = ['frongpath.html', 'wrongpath2.html']
        with self.assertRaises(IOError):
            imgkit.IMGKit('wrongpath.html', 'file')
        with self.assertRaises(IOError):
            imgkit.IMGKit(paths, 'file')

    def test_stylesheet_adding_to_the_head(self):
        # TODO rewrite this part of pdfkit.py
        r = imgkit.IMGKit('<html><head></head><body>Hai!</body></html>', 'string',
                          css='test/fixtures/example.css')

        with open('test/fixtures/example.css') as f:
            css = f.read()

        r._prepend_css('test/fixtures/example.css')
        self.assertIn('<style>%s</style>' % css, r.source.to_s())

    def test_stylesheet_adding_without_head_tag(self):
        r = imgkit.IMGKit('<html><body>Hai!</body></html>', 'string',
                          options={'quiet': None}, css='test/fixtures/example.css')

        with open('test/fixtures/example.css') as f:
            css = f.read()

        r._prepend_css('test/fixtures/example.css')
        self.assertIn('<style>%s</style><html>' % css, r.source.to_s())

    def test_multiple_stylesheets_adding_to_the_head(self):
        # TODO rewrite this part of pdfkit.py
        css_files = ['test/fixtures/example.css', 'test/fixtures/example2.css']
        r = imgkit.IMGKit('<html><head></head><body>Hai!</body></html>', 'string',
                          css=css_files)

        css = []
        for css_file in css_files:
            with open(css_file) as f:
                css.append(f.read())

        r._prepend_css(css_files)
        self.assertIn('<style>%s</style>' % "\n".join(css), r.source.to_s())

    def test_multiple_stylesheet_adding_without_head_tag(self):
        css_files = ['test/fixtures/example.css', 'test/fixtures/example2.css']
        r = imgkit.IMGKit('<html><body>Hai!</body></html>', 'string',
                          options={'quiet': None}, css=css_files)

        css = []
        for css_file in css_files:
            with open(css_file) as f:
                css.append(f.read())

        r._prepend_css(css_files)
        self.assertIn('<style>%s</style><html>' % "\n".join(css), r.source.to_s())

    def test_stylesheet_throw_error_when_url(self):
        r = imgkit.IMGKit('http://ya.ru', 'url', css='test/fixtures/example.css')

        with self.assertRaises(r.SourceError):
            r.to_img()

    def test_stylesheet_adding_to_file_with_option(self):
        css = 'test/fixtures/example.css'
        r = imgkit.IMGKit('test/fixtures/example.html', 'file', css=css)
        self.assertEqual(r.css, css)
        r._prepend_css(css)
        self.assertIn('font-size', r.source.to_s())

    def test_wkhtmltoimage_error_handling(self):
        r = imgkit.IMGKit('clearlywrongurl.asdf', 'url')
        with self.assertRaises(IOError):
            r.to_img()

    def test_pdf_generation_from_file_like(self):
        with open('test/fixtures/example.html', 'r') as f:
            r = imgkit.IMGKit(f, 'file')
            output = r.to_img()
        self.assertEqual(output[:4], b'\xff\xd8\xff\xe0')  # TODO img

    def test_raise_error_with_wrong_css_path(self):
        css = 'test/fixtures/wrongpath.css'
        r = imgkit.IMGKit('test/fixtures/example.html', 'file', css=css)
        with self.assertRaises(IOError):
            r.to_img()

    def test_raise_error_if_bad_wkhtmltoimage_option(self):
        r = imgkit.IMGKit('<html><body>Hai!</body></html>', 'string',
                          options={'bad-option': None})
        with self.assertRaises(IOError) as cm:
            r.to_img()

        raised_exception = cm.exception
        self.assertRegexpMatches(str(raised_exception),
                                 '^wkhtmltoimage exited with non-zero code 1. error:\nUnknown long argument '
                                 '--bad-option\r?\n')


if __name__ == "__main__":
    unittest.main()
