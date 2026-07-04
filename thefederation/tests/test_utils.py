from test_plus import TestCase

from thefederation.utils import clean_hostname, is_valid_hostname


class CleanHostnameTestCase(TestCase):
    def test_strips_protocol_and_whitespace(self):
        self.assertEqual(clean_hostname(' https://Example.COM '), 'example.com')

    def test_protocol_only_becomes_empty(self):
        self.assertEqual(clean_hostname('https://'), '')


class IsValidHostnameTestCase(TestCase):
    def test_valid_hostname(self):
        self.assertTrue(is_valid_hostname('example.com'))
        self.assertTrue(is_valid_hostname('sub.example.com.'))

    def test_empty_hostname_is_invalid(self):
        # Regression: raised IndexError, turning /register/https:// into a 500
        self.assertFalse(is_valid_hostname(''))

    def test_invalid_hostnames(self):
        self.assertFalse(is_valid_hostname('a' * 256))
        self.assertFalse(is_valid_hostname('-bad.example.com'))
        self.assertFalse(is_valid_hostname('exa mple.com'))
