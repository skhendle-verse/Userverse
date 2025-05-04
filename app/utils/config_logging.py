import logging
import json
from datetime import datetime, timezone

import sys

from app.utils.configs import ConfigLoader


class JsonFormatter(logging.Formatter):
    def format(self, record):
        configs = ConfigLoader().get_config()
        app_name = configs.get("app_name", "userverse")
        version = configs.get("version", "1.0.0")
        environment = configs.get("environment", "development")

        log_record = {
            "app_name": app_name,
            "version": version,
            "environment": environment,
            "timestamp": datetime.now(timezone.utc).isoformat(),
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


def setup_logging():
    """Configure application logging to output in JSON format"""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove existing handlers
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)

    # Create and add JSON handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root_logger.addHandler(handler)

    # Set uvicorn access logs to use JSON format too
    uvicorn_logger = logging.getLogger("uvicorn.access")
    uvicorn_logger.handlers = []
    uvicorn_logger.addHandler(handler)

    logging.info("Logging configured with JSON formatter")