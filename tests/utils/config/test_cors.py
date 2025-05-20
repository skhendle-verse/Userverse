import unittest
from app.utils.config.cors import CorsConfig  # Update the path to your actual module


class TestCorsConfig(unittest.TestCase):

    def test_test_environment_returns_default(self):
        config = {}
        result = CorsConfig.get_cors(config, environment="test_environment")
        self.assertEqual(result, CorsConfig.CORS_DEFAULT)

    def test_no_cors_config_returns_default(self):
        config = {}
        result = CorsConfig.get_cors(config, environment="production")
        self.assertEqual(result, CorsConfig.CORS_DEFAULT)

    def test_full_custom_cors_config(self):
        config = {
            "cors": {
                "allowed": ["https://example.com"],
                "blocked": ["http://bad-site.com"]
            }
        }
        result = CorsConfig.get_cors(config, environment="production")
        expected = {
            "allowed": ["https://example.com"],
            "blocked": ["http://bad-site.com"]
        }
        self.assertEqual(result, expected)

    def test_partial_custom_config_falls_back_to_default(self):
        config = {
            "cors": {
                "allowed": ["https://good-site.com"]
            }
        }
        result = CorsConfig.get_cors(config, environment="production")
        expected = {
            "allowed": ["https://good-site.com"],
            "blocked": CorsConfig.CORS_DEFAULT["blocked"]
        }
        self.assertEqual(result, expected)

    def test_empty_cors_dict_returns_default(self):
        config = {"cors": {}}
        result = CorsConfig.get_cors(config, environment="staging")
        self.assertEqual(result, CorsConfig.CORS_DEFAULT)


if __name__ == '__main__':
    unittest.main()
