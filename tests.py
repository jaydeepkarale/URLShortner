""" Test cases for app.py """
import unittest

from src import app

VALID_TEST_URL = "https://www.google.com"
INVALID_TEST_URL = "https:/google.com"


class TestApp(unittest.TestCase):
    """Class contains unittests for app.py functions"""
    def test_get_ngrok_url(self):
        """Function to test if a URL in str format is returned"""
        url = app.get_ngrok_url()
        self.assertIsInstance(url, str)

    def test_validate_long_url_format_validurl(self):
        """Function to test if URL validation return True for valid URL format"""
        self.assertTrue(app.validate_long_url_format(VALID_TEST_URL))

    def test_validate_long_url_format_invalidurl(self):
        """Function to test if URL validation return False for invalid URL format"""
        self.assertFalse(app.validate_long_url_format(INVALID_TEST_URL))

    def test_validate_url_valid_url(self):
        """Function to test if URL validation return True for valid URL"""
        self.assertTrue(app.validate_url(VALID_TEST_URL))

    def test_validate_url_invalid_url(self):
        """Function to test if URL validation return True for invalid URL format"""
        self.assertFalse(app.validate_url(INVALID_TEST_URL))


if __name__ == "__main__":
    unittest.main()
