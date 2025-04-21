# my_app/logging_config.py

import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "mode": "a",
            "formatter": "default",
            "level": "DEBUG",
        },
    },

    # Configure the root logger
    "root": {
        "level": "DEBUG",  # or INFO
        "handlers": ["console", "file"],
    },

    # Module-specific logging (still available if needed)
    "loggers": {
        "uvicorn": {
            "level": "WARNING",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        # Optional app-specific configs can go here
    },
}

_initialized = False

def setup_logging():
    global _initialized
    if not _initialized:
        logging.config.dictConfig(LOGGING_CONFIG)
        _initialized = True
