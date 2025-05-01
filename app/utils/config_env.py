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
            str: The current environment (e.g., 'development', 'production', 'stagging','testing').

        """
        # Check for TEST_ENVIRONMENT in environment variables
        test_environment = os.getenv("TEST_ENVIRONMENT", "").lower() == "true"

        print(f"TEST_ENVIRONMENT: {test_environment}")

        if test_environment:
            return "test_environment"

        # Check for ENVIRONMENT
        # In the provided configuration data
        # or in the environment variables

        if config_data:
            env = config_data.get("env", "").lower()
            if env:
                return env
            env = config_data.get("environment", "").lower()
            if env:
                return env

        env = os.getenv("env", "").lower()
        if env:
            return env
        env = os.getenv("environment", "").lower()
        if env:
            return env

        return "development"
