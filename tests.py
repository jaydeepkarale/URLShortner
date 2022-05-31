import unittest
from src import app


valid_test_url = "https://www.google.com"
invalid_test_url = "https:/google.com"


class TestApp(unittest.TestCase):
    def test_get_ngrok_url(self):
        url = app.get_ngrok_url()
        self.assertIsInstance(url, str)

    def test_validate_long_url_format_validurl(self):
        self.assertTrue(app.validate_long_url_format(valid_test_url))

    def test_validate_long_url_format_invalidurl(self):
        self.assertFalse(app.validate_long_url_format(invalid_test_url))

    def test_validate_url_valid_url(self):
        self.assertTrue(app.validate_url(valid_test_url))

    def test_validate_url_invalid_url(self):
        self.assertFalse(app.validate_url(invalid_test_url))


if __name__ == "__main__":
    unittest.main()
