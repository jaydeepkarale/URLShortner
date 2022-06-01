""" Test cases for app.py """
import unittest

from src import app

valid_test_url = "https://www.google.com"
invalid_test_url = "https:/google.com"


class TestApp(unittest.TestCase):
    def test_get_ngrok_url(self):
        """Function to test if a URL in str format is returned"""
        url = app.get_ngrok_url()
        self.assertIsInstance(url, str)

    def test_validate_long_url_format_validurl(self):
        """Function to test if URL validation return True for valid URL format"""
        self.assertTrue(app.validate_long_url_format(valid_test_url))

    def test_validate_long_url_format_invalidurl(self):
        """Function to test if URL validation return False for invalid URL format"""
        self.assertFalse(app.validate_long_url_format(invalid_test_url))

    def test_validate_url_valid_url(self):
        """Function to test if URL validation return True for valid URL"""
        self.assertTrue(app.validate_url(valid_test_url))

    def test_validate_url_invalid_url(self):
        """Function to test if URL validation return True for invalid URL format"""
        self.assertFalse(app.validate_url(invalid_test_url))


if __name__ == "__main__":
    unittest.main()
