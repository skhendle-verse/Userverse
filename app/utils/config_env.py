import os
from typing import Optional


class EnvironmentManager:

    @classmethod
    def get_environment(cls, config_data: Optional[dict] = None) -> str:
        """
        Determines the current environment based on the TEST_ENVIRONMENT variable
        or the provided configuration data.

        Args:
            config_data (Optional[dict]): A dictionary containing configuration data.
                                          Defaults to None.

        Returns:
            str: The current environment (e.g., 'development', 'production', 'testing').

        """
        # Check for TEST_ENVIRONMENT in environment variables
        test_environment = os.getenv("TEST_ENVIRONMENT")

        if test_environment:
            return "testing"

        environment = os.getenv("ENVIRONMENT")
        if environment:
            return environment

        if config_data and "environment" in config_data:
            return config_data["environment"]

        return "development"
