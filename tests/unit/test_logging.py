"""Unit tests for logging configuration.

Tests the centralized logging setup for the game package.
"""

import logging

from game.config.logging_config import setup_logging


class TestLoggingSetup:
    """Tests for setup_logging function."""

    def test_returns_logger(self) -> None:
        """setup_logging returns a Logger instance."""
        logger = setup_logging()
        assert isinstance(logger, logging.Logger)

    def test_logger_name(self) -> None:
        """Logger is named 'game'."""
        logger = setup_logging()
        assert logger.name == "game"

    def test_default_level_info(self) -> None:
        """Default logging level is INFO."""
        logger = setup_logging(logging.INFO)
        assert logger.level == logging.INFO

    def test_custom_level(self) -> None:
        """Custom logging level is applied."""
        logger = setup_logging(logging.DEBUG)
        assert logger.level == logging.DEBUG

    def test_handler_attached(self) -> None:
        """At least one handler is attached to the logger."""
        logger = setup_logging()
        assert len(logger.handlers) >= 1

    def test_no_duplicate_handlers(self) -> None:
        """Calling setup_logging twice does not add duplicate handlers."""
        logger = setup_logging()
        count = len(logger.handlers)
        setup_logging()
        assert len(logger.handlers) == count
