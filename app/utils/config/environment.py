import os
from typing import Optional


class EnvironmentManager:

    @classmethod
    def get_environment(cls, config_data: Optional[dict] = None) -> str:
        """
        Determines the current environment based on the TEST_ENVIRONMENT variable,
        configuration data, or environment variables.

        Args:
            config_data (Optional[dict]): Optional configuration dictionary.

        Returns:
            str: The current environment ('test_environment', 'development', 'production', etc.).
        """
        if os.getenv("TEST_ENVIRONMENT", "").strip().lower() == "true":
            return "test_environment"

        # Priority-ordered list of environment keys to check
        env_keys = ["env", "environment"]

        # Check in config_data
        if config_data:
            for key in env_keys:
                value = config_data.get(key)
                if value:
                    return value.strip().lower()

        # Check in environment variables
        for key in env_keys:
            value = os.getenv(key, "").strip().lower()
            if value:
                return value

        # Default fallback
        return "development"
