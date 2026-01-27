"""Tests for Pathao SDK exceptions."""

import pytest
from pathao.exceptions import (
    PathaoException,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    APIError,
    NetworkError,
    ConfigurationError,
)


class TestPathaoException:
    """Test base PathaoException class."""

    def test_basic_exception(self):
        """Test basic exception creation."""
        exc = PathaoException("Test error")
        assert str(exc) == "Test error"
        assert exc.message == "Test error"
        assert exc.details == {}

    def test_exception_with_details(self):
        """Test exception with details."""
        details = {"field": "test", "value": "invalid"}
        exc = PathaoException("Test error", details)
        assert exc.details == details

    def test_exception_repr(self):
        """Test exception representation."""
        exc = PathaoException("Test error", {"key": "value"})
        expected = "PathaoException(message='Test error', details={'key': 'value'})"
        assert repr(exc) == expected


class TestAuthenticationError:
    """Test AuthenticationError class."""

    def test_default_message(self):
        """Test default authentication error message."""
        exc = AuthenticationError()
        assert str(exc) == "Authentication failed"

    def test_custom_message(self):
        """Test custom authentication error message."""
        exc = AuthenticationError("Invalid credentials")
        assert str(exc) == "Invalid credentials"

    def test_inheritance(self):
        """Test that AuthenticationError inherits from PathaoException."""
        exc = AuthenticationError()
        assert isinstance(exc, PathaoException)


class TestValidationError:
    """Test ValidationError class."""

    def test_validation_error_creation(self):
        """Test validation error creation."""
        exc = ValidationError("name", "Name is too short")
        assert exc.field == "name"
        assert exc.value is None
        assert "Validation error for 'name': Name is too short" in str(exc)

    def test_validation_error_with_value(self):
        """Test validation error with value."""
        exc = ValidationError("name", "Name is too short", "ab")
        assert exc.field == "name"
        assert exc.value == "ab"
        assert exc.details["field"] == "name"
        assert exc.details["value"] == "ab"


class TestNotFoundError:
    """Test NotFoundError class."""

    def test_not_found_error(self):
        """Test not found error creation."""
        exc = NotFoundError("Store", "123")
        assert exc.resource_type == "Store"
        assert exc.identifier == "123"
        assert "Store with identifier '123' not found" in str(exc)


class TestAPIError:
    """Test APIError class."""

    def test_api_error_basic(self):
        """Test basic API error."""
        exc = APIError("API request failed")
        assert str(exc) == "API request failed"
        assert exc.status_code is None

    def test_api_error_with_status_code(self):
        """Test API error with status code."""
        exc = APIError("Bad request", status_code=400)
        assert exc.status_code == 400
        assert exc.details["status_code"] == 400

    def test_api_error_with_response_data(self):
        """Test API error with response data."""
        response_data = {"error": "Invalid input"}
        exc = APIError("Bad request", response_data=response_data)
        assert exc.response_data == response_data


class TestNetworkError:
    """Test NetworkError class."""

    def test_network_error_basic(self):
        """Test basic network error."""
        exc = NetworkError("Connection timeout")
        assert str(exc) == "Connection timeout"
        assert exc.retry_after is None

    def test_network_error_with_retry(self):
        """Test network error with retry after."""
        exc = NetworkError("Rate limited", retry_after=60)
        assert exc.retry_after == 60
        assert exc.details["retry_after"] == 60


class TestConfigurationError:
    """Test ConfigurationError class."""

    def test_configuration_error_basic(self):
        """Test basic configuration error."""
        exc = ConfigurationError("Missing configuration")
        assert str(exc) == "Missing configuration"
        assert exc.missing_config is None

    def test_configuration_error_with_missing_config(self):
        """Test configuration error with missing config."""
        exc = ConfigurationError("Missing API key", missing_config="client_id")
        assert exc.missing_config == "client_id"
        assert exc.details["missing_config"] == "client_id"
