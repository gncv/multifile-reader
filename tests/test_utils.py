from unittest import TestCase

from multifile_reader.utils import is_url


class IsUrlTestCase(TestCase):
    def test_string(self):
        self.assertFalse(is_url("foo"))

    def test_local_path(self):
        self.assertFalse(is_url("/foo/bar/baz"))

    def test_url(self):
        self.assertTrue(is_url("https://www.example.com/foo"))

    def test_url_with_query_parameters(self):
        self.assertTrue(is_url("https://www.example.com/foo?bar=baz"))
