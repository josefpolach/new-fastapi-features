import logging
import time
from logging.config import dictConfig

from pydantic_settings import BaseSettings, SettingsConfigDict
from pythonjsonlogger import jsonlogger


class Settings(BaseSettings):
    llm_provider: str = "openai"
    openai_api_key: str

    model_config = SettingsConfigDict(env_file=".env")



settings = Settings()


class CustomFormatter(logging.Formatter):
    converter = time.gmtime


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    converter = time.gmtime


def setup_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 32,
                    "default_value": "-",
                },
            },
            "formatters": {
                "console": {
                    "()": CustomFormatter,
                    "datefmt": "%Y-%m-%dT%H:%M:%SZ",
                    "format": "%(asctime)s - %(levelname)s - [%(correlation_id)s] %(name)s - %(message)s",
                },
                "json": {
                    "()": CustomJsonFormatter,
                    "datefmt": "%Y-%m-%dT%H:%M:%SZ",
                    "format": "%(asctime)s %(levelname)s [%(correlation_id)s] %(name)s %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "filters": ["correlation_id"],
                    "formatter": "console",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "formatter": "json",
                    "filename": "app.log",
                    "encoding": "utf-8",
                },
            },
            "loggers": {
                "app": {
                    "handlers": ["console", "file"],
                    "level": "INFO",
                    "propagate": False,
                },
                "uvicorn": {
                    "handlers": ["console", "file"],
                    "level": "INFO",
                },
            },
        },
    )
