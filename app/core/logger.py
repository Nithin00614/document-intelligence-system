"""
Centralized logger configuration.
Every module should import this logger.
"""

import sys
from loguru import logger

from app.core.config import settings

# Remove default logger
logger.remove()

# Console logging
logger.add(
    sys.stdout,
    level=settings.LOG_LEVEL,
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
)

# File logging
logger.add(
    settings.LOG_DIR / "application.log",
    level=settings.LOG_LEVEL,
    rotation="10 MB",
    retention="7 days",
    compression="zip",
)

__all__ = ["logger"]