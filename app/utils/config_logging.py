# In app/utils/config_logging.py
import logging
import json
from datetime import datetime

from app.utils.configs import ConfigLoader

class JsonFormatter(logging.Formatter):
    def __init__(self, *args, use_colors=None, **kwargs):
        # Ignore use_colors parameter that Uvicorn tries to pass
        super().__init__(*args, **kwargs)

    def format(self, record):
        configs = ConfigLoader().get_config()
        app_name = configs.get("app_name", "userverse")
        version = configs.get("version", "1.0.0")

        log_record = {
            "app_name": app_name,
            "version": version,
            "environment": configs.get("environment", "development"),
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if hasattr(record, "request_id"):
            log_record["request_id"] = record.request_id

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)