"""Custom exceptions for Pathao Python SDK."""

from typing import Optional


class PathaoException(Exception):
    """Base exception for all Pathao SDK errors."""

    def __init__(self, message: str, details: Optional[dict] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(message='{self.message}', "
            f"details={self.details})"
        )


class AuthenticationError(PathaoException):
    """Raised when authentication fails or token refresh fails."""

    def __init__(
        self, message: str = "Authentication failed", details: Optional[dict] = None
    ):
        super().__init__(message, details)


class ValidationError(PathaoException):
    """Raised when input validation fails."""

    def __init__(self, field: str, message: str, value: Optional[str] = None):
        self.field = field
        self.value = value
        details = {"field": field, "value": value}
        super().__init__(f"Validation error for '{field}': {message}", details)


class NotFoundError(PathaoException):
    """Raised when requested resource is not found."""

    def __init__(self, resource_type: str, identifier: str):
        self.resource_type = resource_type
        self.identifier = identifier
        message = f"{resource_type} with identifier '{identifier}' not found"
        details = {"resource_type": resource_type, "identifier": identifier}
        super().__init__(message, details)


class APIError(PathaoException):
    """Raised for general API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[dict] = None,
    ):
        self.status_code = status_code
        self.response_data = response_data or {}
        details = {"status_code": status_code, "response_data": response_data}
        super().__init__(message, details)


class NetworkError(PathaoException):
    """Raised for network-related failures."""

    def __init__(self, message: str, retry_after: Optional[int] = None):
        self.retry_after = retry_after
        details = {"retry_after": retry_after}
        super().__init__(message, details)


class ConfigurationError(PathaoException):
    """Raised for configuration issues."""

    def __init__(self, message: str, missing_config: Optional[str] = None):
        self.missing_config = missing_config
        details = {"missing_config": missing_config}
        super().__init__(message, details)
