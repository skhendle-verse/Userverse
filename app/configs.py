import json
from app.utils.db_config import DatabaseConfig


with open("sample-config.json") as f:
    data = json.load(f)


environment = data.get("environment", "dev")
configs = {
    "environment": environment,
    "database_url": DatabaseConfig.get_connection_string(data, environment),
}
