import logging
import sys
import structlog
from typing import Optional, Union, Dict, Any
from starlette import status

_logger = None  # Global logger reference

def setup_logging():
    global _logger  # ✅ This is essential

    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        cache_logger_on_first_use=True,
    )

    _logger = structlog.get_logger()
    return _logger

def get_logger():
    if _logger is None:
        raise RuntimeError("Logger not initialized. Call setup_logging() first.")
    return _logger
