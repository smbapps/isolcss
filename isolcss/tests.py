from __future__ import unicode_literals

from main import isolcss
import logging
import os
import unittest


logging.basicConfig()


if os.path.exists('testdata'):
    TESTDATA = 'testdata'
else:
    TESTDATA = 'isolcss/testdata'

assert os.path.exists(TESTDATA)


class TestIsolCss(unittest.TestCase):
    def test_simple(self):
        given = "p, .class > x[name=foo] { rules; }"
        expected = "#X p, #X .class > x[name=foo] { rules; }"
        actual = isolcss('#X', given)
        self.assertEqual(actual, expected)

    def test_replace(self):
        given = "p, .class > &.x[name=foo] { rules; }"
        expected = "#X p, .class > #X.x[name=foo] { rules; }"
        actual = isolcss('#X', given)
        self.assertEqual(actual, expected)

    def _test_css_file(self, filename):
        inf = os.path.join(TESTDATA, filename)
        outf = inf + '.out'
        with open(inf) as f:
            given = f.read()
        actual = isolcss('#X', given)
        if os.environ.get('UPDATE_TEST_OUTPUT'):
            with open(outf, 'w') as f:
                f.write(actual)
        with open(outf) as f:
            expected = f.read()
        self.assertEqual(actual, expected)

    def test_bootstrap(self):
        self._test_css_file('bootstrap.css')

    def test_bootstrap_min(self):
        self._test_css_file('bootstrap.min.css')

    def test_bootstrap_resp(self):
        self._test_css_file('bootstrap-responsive.css')

    def test_bootstrap_resp_min(self):
        self._test_css_file('bootstrap-responsive.min.css')


if __name__ == '__main__':
    unittest.main()
