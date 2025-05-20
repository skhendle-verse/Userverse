import unittest
from unittest.mock import patch
from app.utils.config.environment import EnvironmentManager  # Replace with your actual module name


class TestEnvironmentManager(unittest.TestCase):

    @patch.dict('os.environ', {'TEST_ENVIRONMENT': 'true'})
    def test_test_environment_variable(self):
        self.assertEqual(EnvironmentManager.get_environment(), "test_environment")

    def test_config_data_env_key(self):
        config = {"env": "production"}
        self.assertEqual(EnvironmentManager.get_environment(config), "production")

    def test_config_data_environment_key(self):
        config = {"environment": "staging"}
        self.assertEqual(EnvironmentManager.get_environment(config), "staging")

    @patch.dict('os.environ', {'env': 'testing'})
    def test_env_variable(self):
        self.assertEqual(EnvironmentManager.get_environment(), "testing")

    @patch.dict('os.environ', {'environment': 'qa'})
    def test_environment_variable(self):
        self.assertEqual(EnvironmentManager.get_environment(), "qa")

    def test_default_development(self):
        self.assertEqual(EnvironmentManager.get_environment(), "development")

    @patch.dict('os.environ', {'TEST_ENVIRONMENT': 'false', 'env': '', 'environment': ''})
    def test_empty_environment_variables(self):
        self.assertEqual(EnvironmentManager.get_environment(), "development")

    def test_config_data_with_empty_values(self):
        config = {"env": "", "environment": ""}
        self.assertEqual(EnvironmentManager.get_environment(config), "development")


if __name__ == '__main__':
    # uv run -m tests.utils.config.test_environment_manager
    unittest.main()
