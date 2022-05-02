import logging.config
from settings import Config


def setup_logger(config: Config) -> None:
    default_logging = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "colored_console": {
                "format": "[%(asctime)s][%(levelname)s] in %(module)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "colored_console"
            }
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": config.logger["level"]
            }
        }
    }
    logging.config.dictConfig(default_logging)
