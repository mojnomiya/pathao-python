"""Tests for Pathao SDK logger."""

import logging
from pathao.logger import get_logger, setup_logging, SensitiveDataFormatter


class TestGetLogger:
    """Test get_logger function."""

    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a logger instance."""
        logger = get_logger("test_logger")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger"

    def test_get_logger_has_handler(self):
        """Test that logger has a handler configured."""
        logger = get_logger("test_logger_handler")
        assert len(logger.handlers) > 0

    def test_get_logger_level(self):
        """Test that logger has correct level."""
        logger = get_logger("test_logger_level")
        assert logger.level == logging.INFO


class TestSetupLogging:
    """Test setup_logging function."""

    def test_setup_logging_default_level(self):
        """Test setup_logging with default level."""
        setup_logging()
        logger = logging.getLogger("pathao")
        assert logger.level == logging.INFO

    def test_setup_logging_debug_level(self):
        """Test setup_logging with debug level."""
        setup_logging("DEBUG")
        logger = logging.getLogger("pathao")
        assert logger.level == logging.DEBUG

    def test_setup_logging_invalid_level(self):
        """Test setup_logging with invalid level defaults to INFO."""
        setup_logging("INVALID")
        logger = logging.getLogger("pathao")
        assert logger.level == logging.INFO


class TestSensitiveDataFormatter:
    """Test SensitiveDataFormatter class."""

    def setup_method(self):
        """Setup test method."""
        self.formatter = SensitiveDataFormatter("%(message)s")

    def test_mask_access_token(self):
        """Test masking access token."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg='{"access_token": "secret_token_123"}',
            args=(),
            exc_info=None,
        )

        formatted = self.formatter.format(record)
        assert "secret_token_123" not in formatted
        assert "***MASKED***" in formatted

    def test_mask_refresh_token(self):
        """Test masking refresh token."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg='{"refresh_token": "refresh_secret_456"}',
            args=(),
            exc_info=None,
        )

        formatted = self.formatter.format(record)
        assert "refresh_secret_456" not in formatted
        assert "***MASKED***" in formatted

    def test_mask_password(self):
        """Test masking password."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg='{"password": "my_secret_password"}',
            args=(),
            exc_info=None,
        )

        formatted = self.formatter.format(record)
        assert "my_secret_password" not in formatted
        assert "***MASKED***" in formatted

    def test_mask_client_secret(self):
        """Test masking client secret."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg='{"client_secret": "client_secret_789"}',
            args=(),
            exc_info=None,
        )

        formatted = self.formatter.format(record)
        assert "client_secret_789" not in formatted
        assert "***MASKED***" in formatted

    def test_mask_authorization_header(self):
        """Test masking authorization header."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
            args=(),
            exc_info=None,
        )

        formatted = self.formatter.format(record)
        assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in formatted
        assert "***MASKED***" in formatted

    def test_mask_token_parameter(self):
        """Test masking token parameter."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Request URL: https://api.example.com/data?token=abc123&other=value",
            args=(),
            exc_info=None,
        )

        formatted = self.formatter.format(record)
        assert "abc123" not in formatted
        assert "***MASKED***" in formatted

    def test_no_masking_for_safe_content(self):
        """Test that safe content is not masked."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg='{"user_id": 123, "order_id": "ORD001"}',
            args=(),
            exc_info=None,
        )

        formatted = self.formatter.format(record)
        assert "user_id" in formatted
        assert "order_id" in formatted
        assert "***MASKED***" not in formatted

    def test_case_insensitive_masking(self):
        """Test that masking is case insensitive."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg='{"ACCESS_TOKEN": "secret_token_123"}',
            args=(),
            exc_info=None,
        )

        formatted = self.formatter.format(record)
        assert "secret_token_123" not in formatted
        assert "***MASKED***" in formatted
