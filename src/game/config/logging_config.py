"""Logging configuration for Conway's Game of Life.

Provides a centralized logging setup for consistent log formatting
and level management across all game modules.
"""

import logging
import sys


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure and return the root game logger.

    Sets up a console handler with a structured format including
    timestamps, module names, and log levels.

    Args:
        level: Logging level (e.g., logging.DEBUG, logging.INFO).

    Returns:
        Configured root logger for the game package.
    """
    logger = logging.getLogger("game")
    logger.setLevel(level)

    # Avoid duplicate handlers if called multiple times
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
