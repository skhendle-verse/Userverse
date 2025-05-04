import os
import logging
import json
import sys
from pathlib import Path
from app.utils.config_db import DatabaseConfig
from app.utils.config_env import EnvironmentManager

# Use built-in tomllib for Python 3.11+, otherwise use tomli
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

cors_default = {
    "allowed": ["*"],
    "blocked": ["http://localhost:30XX"],
}


class ConfigLoader:
    def __init__(self, environment: str = None):
        json_config_path = os.getenv("JSON_CONFIG_PATH", None)
        if json_config_path:
            json_config_path = Path(json_config_path).resolve()
            if not json_config_path.exists():
                raise ValueError(f"JSON config file does not exist: {json_config_path}")
            self.json_config_path = json_config_path
        self.environment = environment
        self.config = self._load_config()

    def _set_environment(self, config_data):
        """
        Sets the environment for the configuration.
        Args:
            config_data (dict): Configuration data.
        """
        if self.environment:
            return self.environment
        else:
            return EnvironmentManager.get_environment(config_data)

    def _load_config(self):

        if self.json_config_path:
            try:
                return self._load_from_json()
            except Exception as e:
                raise ValueError(f"Error loading JSON configuration: {e}")
        config = self._load_from_toml()
        return config

    def _load_from_toml(self):
        try:
            logging.info("Loading configuration from pyproject.toml")
            pyproject_path = Path(__file__).resolve().parent.parent / "pyproject.toml"

            if not pyproject_path.exists():
                return None

            with open(pyproject_path, "rb") as f:
                pyproject_data = tomllib.load(f)

            app_config = (
                pyproject_data.get("tool", {}).get("userverse", {}).get("config", {})
            )

            if not app_config:
                raise ValueError(
                    "No configuration found in pyproject.toml under [tool.uservese.config]"
                )

            environment = self._set_environment(app_config)
            return {
                "environment": environment,
                "database_url": DatabaseConfig.get_connection_string(
                    app_config, environment
                ),
                "cor_origins": app_config.get("cor_origins", cors_default),
                "jwt": app_config.get("jwt", {}),
                "email": app_config.get("email", {}),
                "version": app_config.get("version", "0.1.0"),
                "name": app_config.get("name", "Userverse"),
                "description": app_config.get("description", "Userverse backend API"),
            }

        except Exception as e:
            logging.error("Error loading configuration from pyproject.toml: %s", e)
            raise ValueError("Error loading configuration from pyproject.toml: %s", e)

    def _load_from_json(self):
        try:
            logging.info("Loading configuration from JSON")
            with open(self.json_config_path) as f:
                data = json.load(f)

            environment = self._set_environment(data)
            return {
                "environment": environment,
                "database_url": DatabaseConfig.get_connection_string(data, environment),
                "cor_origins": data.get("cors_origins", cors_default),
                "jwt": data.get("jwt", {}),
                "email": data.get("email", {}),
                "version": data.get("version", "0.1.0"),
                "name": data.get("name", "Userverse"),
                "description": data.get("description", "Userverse backend API"),
            }

        except Exception as e:
            logging.error("Error loading configuration from JSON: %s", e)
            raise ValueError(f"Error loading configuration: {e}")

    def get_config(self):
        return self.config
