import logging.config
import multiprocessing

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [PID %(process)d] [%(levelname)s] %(name)s: %(message)s",
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
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
    "loggers": {
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "uvicorn.access": {
            "level": "WARNING",  # Change to INFO for detailed request logs
            "handlers": ["console", "file"],
            "propagate": False,
        },
        # Optional custom loggers can go here
    },
}

_initialized = False


def setup_logging():
    global _initialized
    if not _initialized:
        logging.config.dictConfig(LOGGING_CONFIG)
        _initialized = True

        # Optional: show startup message with PID
        logger = logging.getLogger(__name__)
        logger.info(
            f"✅ Logging configured [PID {multiprocessing.current_process().pid}]"
        )
