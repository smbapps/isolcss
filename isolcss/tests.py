from __future__ import unicode_literals

from main import isolcss
import unittest


class IsolCssTestCase(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
