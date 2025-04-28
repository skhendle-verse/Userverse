import os
import json
from app.utils.db_config import DatabaseConfig
from app.utils.env_config import EnvironmentManager

try:
    with open("app/sample-config.json") as f:
        data = json.load(f)

    environment = EnvironmentManager.get_environment(data)
    configs = {
        "environment": environment,
        "database_url": DatabaseConfig.get_connection_string(data, environment),
        "cor_origins": data.get("cors_origins", ["*"]),
        "jwt": data.get("jwt", {}),
    }
except Exception as e:
    raise ValueError(f"Error loading configuration: {e}")
