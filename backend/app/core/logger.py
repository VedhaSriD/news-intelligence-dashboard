"""
core/logger.py
Structured UTC logging. Call setup_logging() once at startup.
"""
import logging
import sys
from datetime import datetime, timezone


class UTCFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        return datetime.fromtimestamp(
            record.created, tz=timezone.utc
        ).strftime("%Y-%m-%dT%H:%M:%SZ")

    def format(self, record):
        level   = record.levelname.ljust(8)
        time    = self.formatTime(record)
        name    = record.name.split(".")[-1]
        message = record.getMessage()
        base    = f"{time} {level} [{name}] {message}"
        if record.exc_info:
            base += "\n" + self.formatException(record.exc_info)
        return base


def setup_logging(level: str = "INFO") -> None:
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    root.handlers.clear()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(UTCFormatter())
    root.addHandler(handler)
    for noisy in ["httpx", "httpcore", "uvicorn.access", "apscheduler"]:
        logging.getLogger(noisy).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)