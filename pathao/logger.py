"""Logging configuration for Pathao Python SDK."""

import logging
import re


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with proper configuration."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = SensitiveDataFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration for the SDK."""
    log_level = getattr(logging, level.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Set specific logger for pathao
    pathao_logger = logging.getLogger("pathao")
    pathao_logger.setLevel(log_level)


class SensitiveDataFormatter(logging.Formatter):
    """Custom formatter that masks sensitive data in log messages."""

    SENSITIVE_PATTERNS = [
        (r'("access_token":\s*")[^"]*(")', r"\1***MASKED***\2"),
        (r'("refresh_token":\s*")[^"]*(")', r"\1***MASKED***\2"),
        (r'("password":\s*")[^"]*(")', r"\1***MASKED***\2"),
        (r'("client_secret":\s*")[^"]*(")', r"\1***MASKED***\2"),
        (r"(Authorization:\s*Bearer\s+)[^\s]+", r"\1***MASKED***"),
        (r"(token=)[^\s&]+", r"\1***MASKED***"),
    ]

    def format(self, record: logging.LogRecord) -> str:
        """Format log record while masking sensitive data."""
        formatted = super().format(record)

        for pattern, replacement in self.SENSITIVE_PATTERNS:
            formatted = re.sub(pattern, replacement, formatted, flags=re.IGNORECASE)

        return formatted
