import unittest

from uspider import USpider


class TestUSpider(unittest.TestCase):
    def test_parse_link(self):
        uspider = USpider(name="test")
        uspider.allowed_domains = ['test.com']

        test_http = uspider.parse_link('', 'http://test.com')
        self.assertEqual(test_http['type'], 'internal')

        test_https = uspider.parse_link('', 'https://test.com')
        self.assertEqual(test_https['type'], 'internal')

        test_subdomain = uspider.parse_link('', 'https://abra.test.com')
        self.assertEqual(test_subdomain['type'], 'subdomain')

        test_external = uspider.parse_link('', 'http://external.com')
        self.assertEqual(test_external['type'], 'external')

        test_reverse = uspider.parse_link('', 'http://test.external.com')
        self.assertEqual(test_reverse['type'], 'external')

    def test_parse(self):
        pass

if __name__ == '__main__':
    unittest.main()
