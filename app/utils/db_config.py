class DatabaseConfig:
    """
    Database configuration class.
    """

    @classmethod
    def get_connection_string(cls, configs, environment="dev") -> str:
        """
        Returns the connection string for the database.
        """
        url = ""
        if environment == "prod":
            db_config = configs.get("database", {})
            db_type = db_config.get("type")
            host = db_config.get("host")
            port = db_config.get("port")
            user = db_config.get("user")
            password = db_config.get("password")
            db_name = db_config.get("db_name")

            if db_type == "postgresql":
                url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
            elif db_type == "mysql":
                url = f"mysql://{user}:{password}@{host}:{port}/{db_name}"
            else:
                raise ValueError(f"Unsupported database type: {db_type}")
        else:
            url = f"sqlite:///{environment}.db"

        return url
