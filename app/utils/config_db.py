class DatabaseConfig:
    """
    Database configuration class.
    """

    @classmethod
    def get_connection_string(cls, configs, environment="development") -> str:
        """
        Returns the connection string for the database.
        Args:
            configs (dict): Configuration data.
            environment (str): The current environment (e.g., 'development', 'production', 'testing').
        Returns:
            str: The connection string for the database.
        """
        if environment == "test_environment":
            return f"sqlite:///testing_{environment}.db"

        db_config = configs.get("database", {})
        if db_config:
            db_type = db_config.get("TYPE")
            host = db_config.get("HOST")
            port = db_config.get("PORT")
            user = db_config.get("USERNAME")
            password = db_config.get("PASSWORD")
            db_name = db_config.get("NAME")

            if db_type == "postgresql":
                return (
                    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
                )
            elif db_type == "mysql":
                return f"mysql://{user}:{password}@{host}:{port}/{db_name}"
            else:
                raise ValueError(f"Unsupported database type: {db_type}")
        else:
            url = f"sqlite:///{environment}.db"

        return url
