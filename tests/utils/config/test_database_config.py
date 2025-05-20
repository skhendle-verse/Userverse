import unittest
from unittest.mock import patch
from app.utils.config.database import DatabaseConfig  # adjust to match your actual path


class TestDatabaseConfigWithLogging(unittest.TestCase):

    @patch("app.utils.config.database.logger")
    def test_test_environment_sqlite(self, mock_logger):
        config = {}
        result = DatabaseConfig.get_connection_string(
            config, environment="test_environment"
        )
        self.assertEqual(result, "sqlite:///test_environment.db")
        mock_logger.warning.assert_not_called()

    @patch("app.utils.config.database.logger")
    def test_no_database_config(self, mock_logger):
        config = {}
        result = DatabaseConfig.get_connection_string(config, environment="dev")
        self.assertEqual(result, "sqlite:///dev.db")
        mock_logger.warning.assert_called_with(
            "No database config found. Falling back to SQLite."
        )

    @patch("app.utils.config.database.logger")
    def test_missing_fields_fallback_to_sqlite(self, mock_logger):
        config = {
            "database": {
                "TYPE": "postgresql",
                "HOST": "localhost",
                # Missing PORT, USER, PASSWORD, NAME
            }
        }
        result = DatabaseConfig.get_connection_string(config, environment="production")
        self.assertEqual(result, "sqlite:///production.db")
        mock_logger.warning.assert_called()
        self.assertIn(
            "Missing database config fields", mock_logger.warning.call_args[0][0]
        )

    @patch("app.utils.config.database.logger")
    def test_unsupported_type_fallback(self, mock_logger):
        config = {
            "database": {
                "TYPE": "oracle",
                "HOST": "localhost",
                "PORT": "1234",
                "USER": "admin",
                "PASSWORD": "secret",
                "NAME": "testdb",
            }
        }
        result = DatabaseConfig.get_connection_string(config, environment="prod")
        self.assertEqual(result, "sqlite:///prod.db")
        mock_logger.warning.assert_called_with(
            "Unsupported database type: 'oracle'. Falling back to SQLite."
        )

    def test_postgresql_connection_string(self):
        config = {
            "database": {
                "TYPE": "postgresql",
                "HOST": "localhost",
                "PORT": "5432",
                "USER": "postgres",
                "PASSWORD": "pass",
                "NAME": "mydb",
            }
        }
        result = DatabaseConfig.get_connection_string(config, environment="production")
        self.assertEqual(
            result, "postgresql+psycopg2://postgres:pass@localhost:5432/mydb"
        )

    def test_mysql_connection_string(self):
        config = {
            "database": {
                "TYPE": "mysql",
                "HOST": "127.0.0.1",
                "PORT": "3306",
                "USER": "root",
                "PASSWORD": "toor",
                "NAME": "sampledb",
            }
        }
        result = DatabaseConfig.get_connection_string(config)
        self.assertEqual(result, "mysql://root:toor@127.0.0.1:3306/sampledb")

    def test_sqlite_explicit_config(self):
        config = {"database": {"TYPE": "sqlite", "NAME": "custom.db"}}
        result = DatabaseConfig.get_connection_string(config, environment="any")
        self.assertEqual(result, "sqlite:///custom.db")


if __name__ == "__main__":
    unittest.main()
