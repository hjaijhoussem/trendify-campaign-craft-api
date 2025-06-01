import sys

from asgi_correlation_id.context import correlation_id
from loguru import logger

from core.config import cfg


def configure():
    def correlation_id_filter(record):
        record["correlation_id"] = correlation_id.get()
        return record["correlation_id"]

    logger.remove()
    fmt = "{level}: \t  {time} {name}:{line} [{correlation_id}] - {message}"
    # Temporarily force DEBUG level for troubleshooting
    logger.add(sys.stderr, format=fmt, level=cfg.LOG_LEVEL, filter=correlation_id_filter)