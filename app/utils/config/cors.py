from app.utils.config.logging import logger


class CorsConfig:
    """
    Database configuration class.
    """

    CORS_DEFAULT = {
        "allowed": ["*"],
        "blocked": ["http://localhost:30XX"],
    }

    @classmethod
    def get_cors(cls, configs:dict, environment="development") -> dict:
        """
        Returns the connection string for the database.
        Args:
            configs (dict): Configuration data.
            environment (str): The current environment (e.g., 'development', 'production', 'testing').
        Returns:
            str: The connection string for the database.
        """
        if environment == "test_environment":
            return cls.CORS_DEFAULT
        
        cors_config = configs.get("cors", {})
        if cors_config:
            allowed = cors_config.get("allowed", cls.CORS_DEFAULT["allowed"])
            blocked = cors_config.get("blocked", cls.CORS_DEFAULT["blocked"])
            return {
                "allowed": allowed,
                "blocked": blocked
            }
        
        return cls.CORS_DEFAULT