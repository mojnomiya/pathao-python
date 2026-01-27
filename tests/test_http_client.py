"""Tests for Pathao SDK HTTP client."""

import json
import pytest
from unittest.mock import Mock, patch
import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout, RequestException

from pathao.http_client import HTTPClient
from pathao.exceptions import APIError, NetworkError


class TestHTTPClientInitialization:
    """Test HTTPClient initialization."""

    def test_init_default_values(self):
        """Test initialization with default values."""
        client = HTTPClient("https://api.example.com")
        assert client.base_url == "https://api.example.com"
        assert client.timeout == 30
        assert client.max_retries == 3
        assert client.retry_backoff == 0.3

    def test_init_custom_values(self):
        """Test initialization with custom values."""
        client = HTTPClient(
            "https://api.example.com/",
            timeout=60,
            max_retries=5,
            retry_backoff=0.5,
        )
        assert client.base_url == "https://api.example.com"
        assert client.timeout == 60
        assert client.max_retries == 5
        assert client.retry_backoff == 0.5

    def test_base_url_trailing_slash_removed(self):
        """Test that trailing slash is removed from base URL."""
        client = HTTPClient("https://api.example.com/")
        assert client.base_url == "https://api.example.com"


class TestHTTPClientGet:
    """Test HTTPClient GET requests."""

    def setup_method(self):
        """Setup test method."""
        self.client = HTTPClient("https://api.example.com")

    @patch("pathao.http_client.requests.Session.get")
    def test_get_success(self, mock_get):
        """Test successful GET request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.client.get("/test")

        assert result == {"success": True}
        mock_get.assert_called_once_with(
            "https://api.example.com/test",
            headers={"Content-Type": "application/json"},
            params=None,
            timeout=30,
        )

    @patch("pathao.http_client.requests.Session.get")
    def test_get_with_params_and_headers(self, mock_get):
        """Test GET request with parameters and headers."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        headers = {"Authorization": "Bearer token"}
        params = {"page": 1, "limit": 10}

        result = self.client.get("/test", headers=headers, params=params)

        assert result == {"data": []}
        mock_get.assert_called_once_with(
            "https://api.example.com/test",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer token",
            },
            params=params,
            timeout=30,
        )

    @patch("pathao.http_client.requests.Session.get")
    def test_get_json_decode_error(self, mock_get):
        """Test GET request with JSON decode error."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.text = "Invalid response"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(APIError) as exc_info:
            self.client.get("/test")

        assert "Invalid JSON response" in str(exc_info.value)
        assert exc_info.value.status_code == 200


class TestHTTPClientPost:
    """Test HTTPClient POST requests."""

    def setup_method(self):
        """Setup test method."""
        self.client = HTTPClient("https://api.example.com")

    @patch("pathao.http_client.requests.Session.post")
    def test_post_success(self, mock_post):
        """Test successful POST request."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 123}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        data = {"name": "test"}
        result = self.client.post("/test", data=data)

        assert result == {"id": 123}
        mock_post.assert_called_once_with(
            "https://api.example.com/test",
            headers={"Content-Type": "application/json"},
            data='{"name": "test"}',
            timeout=30,
        )

    @patch("pathao.http_client.requests.Session.post")
    def test_post_without_data(self, mock_post):
        """Test POST request without data."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.client.post("/test")

        assert result == {"success": True}
        mock_post.assert_called_once_with(
            "https://api.example.com/test",
            headers={"Content-Type": "application/json"},
            data=None,
            timeout=30,
        )


class TestHTTPClientErrorHandling:
    """Test HTTPClient error handling."""

    def setup_method(self):
        """Setup test method."""
        self.client = HTTPClient("https://api.example.com", max_retries=2)

    @patch("pathao.http_client.requests.Session.get")
    def test_timeout_error_no_retry(self, mock_get):
        """Test timeout error without retry."""
        mock_get.side_effect = Timeout("Request timeout")

        with pytest.raises(NetworkError) as exc_info:
            self.client.get("/test")

        assert "Request timeout after 30s" in str(exc_info.value)
        assert mock_get.call_count == 3  # Initial + 2 retries

    @patch("pathao.http_client.requests.Session.get")
    def test_connection_error_with_retry(self, mock_get):
        """Test connection error with retry."""
        mock_get.side_effect = ConnectionError("Connection failed")

        with pytest.raises(NetworkError) as exc_info:
            self.client.get("/test")

        assert "Connection error" in str(exc_info.value)
        assert mock_get.call_count == 3  # Initial + 2 retries

    @patch("pathao.http_client.requests.Session.get")
    def test_http_error_4xx_no_retry(self, mock_get):
        """Test HTTP 4xx error (no retry)."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.reason = "Bad Request"
        mock_response.json.return_value = {"error": "Invalid input"}

        http_error = HTTPError("400 Client Error")
        http_error.response = mock_response
        mock_get.side_effect = http_error

        with pytest.raises(APIError) as exc_info:
            self.client.get("/test")

        assert exc_info.value.status_code == 400
        assert "HTTP 400: Bad Request" in str(exc_info.value)
        assert mock_get.call_count == 1  # No retry for 4xx

    @patch("pathao.http_client.requests.Session.get")
    def test_http_error_5xx_with_retry(self, mock_get):
        """Test HTTP 5xx error (with retry)."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.reason = "Internal Server Error"
        mock_response.json.return_value = {"error": "Server error"}

        http_error = HTTPError("500 Server Error")
        http_error.response = mock_response
        mock_get.side_effect = http_error

        with pytest.raises(APIError) as exc_info:
            self.client.get("/test")

        assert exc_info.value.status_code == 500
        assert "HTTP 500: Internal Server Error" in str(exc_info.value)
        assert mock_get.call_count == 3  # Initial + 2 retries

    @patch("pathao.http_client.requests.Session.get")
    def test_http_error_json_decode_error(self, mock_get):
        """Test HTTP error with JSON decode error."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.reason = "Bad Request"
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.text = "Error response"

        http_error = HTTPError("400 Client Error")
        http_error.response = mock_response
        mock_get.side_effect = http_error

        with pytest.raises(APIError) as exc_info:
            self.client.get("/test")

        assert exc_info.value.status_code == 400
        assert exc_info.value.response_data["raw_response"] == "Error response"

    @patch("pathao.http_client.requests.Session.get")
    def test_request_exception_with_retry(self, mock_get):
        """Test general request exception with retry."""
        mock_get.side_effect = RequestException("Request failed")

        with pytest.raises(NetworkError) as exc_info:
            self.client.get("/test")

        assert "Request failed" in str(exc_info.value)
        assert mock_get.call_count == 3  # Initial + 2 retries


class TestHTTPClientRetryLogic:
    """Test HTTPClient retry logic."""

    def setup_method(self):
        """Setup test method."""
        self.client = HTTPClient("https://api.example.com", max_retries=2)

    def test_should_retry_timeout(self):
        """Test should retry on timeout."""
        assert self.client._should_retry(Timeout(), 0) is True
        assert self.client._should_retry(Timeout(), 1) is True
        assert self.client._should_retry(Timeout(), 2) is False

    def test_should_retry_connection_error(self):
        """Test should retry on connection error."""
        assert self.client._should_retry(ConnectionError(), 0) is True
        assert self.client._should_retry(ConnectionError(), 2) is False

    def test_should_retry_http_error_5xx(self):
        """Test should retry on 5xx HTTP error."""
        mock_response = Mock()
        mock_response.status_code = 500
        http_error = HTTPError()
        http_error.response = mock_response

        assert self.client._should_retry(http_error, 0) is True
        assert self.client._should_retry(http_error, 2) is False

    def test_should_retry_http_error_4xx(self):
        """Test should not retry on 4xx HTTP error."""
        mock_response = Mock()
        mock_response.status_code = 400
        http_error = HTTPError()
        http_error.response = mock_response

        assert self.client._should_retry(http_error, 0) is False

    def test_should_retry_request_exception(self):
        """Test should retry on request exception."""
        assert self.client._should_retry(RequestException(), 0) is True
        assert self.client._should_retry(RequestException(), 2) is False

    def test_should_retry_other_exception(self):
        """Test should not retry on other exceptions."""
        assert self.client._should_retry(ValueError(), 0) is False

    @patch("pathao.http_client.time.sleep")
    def test_exponential_backoff(self, mock_sleep):
        """Test exponential backoff calculation."""
        self.client._exponential_backoff(0)
        mock_sleep.assert_called_with(0.3)

        self.client._exponential_backoff(1)
        mock_sleep.assert_called_with(0.6)

        self.client._exponential_backoff(2)
        mock_sleep.assert_called_with(1.2)


class TestHTTPClientSuccessfulRetry:
    """Test HTTPClient successful retry scenarios."""

    def setup_method(self):
        """Setup test method."""
        self.client = HTTPClient("https://api.example.com", max_retries=2)

    @patch("pathao.http_client.time.sleep")
    @patch("pathao.http_client.requests.Session.get")
    def test_retry_success_after_timeout(self, mock_get, mock_sleep):
        """Test successful request after timeout retry."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_response.raise_for_status.return_value = None

        # First call times out, second succeeds
        mock_get.side_effect = [Timeout("Timeout"), mock_response]

        result = self.client.get("/test")

        assert result == {"success": True}
        assert mock_get.call_count == 2
        mock_sleep.assert_called_once_with(0.3)

    @patch("pathao.http_client.time.sleep")
    @patch("pathao.http_client.requests.Session.get")
    def test_retry_success_after_server_error(self, mock_get, mock_sleep):
        """Test successful request after server error retry."""
        mock_error_response = Mock()
        mock_error_response.status_code = 500
        mock_error_response.reason = "Internal Server Error"
        mock_error_response.json.return_value = {"error": "Server error"}

        mock_success_response = Mock()
        mock_success_response.status_code = 200
        mock_success_response.json.return_value = {"success": True}
        mock_success_response.raise_for_status.return_value = None

        http_error = HTTPError("500 Server Error")
        http_error.response = mock_error_response

        # First call fails with 500, second succeeds
        mock_get.side_effect = [http_error, mock_success_response]

        result = self.client.get("/test")

        assert result == {"success": True}
        assert mock_get.call_count == 2
        mock_sleep.assert_called_once_with(0.3)


class TestHTTPClientUnsupportedMethod:
    """Test HTTPClient with unsupported HTTP method."""

    def setup_method(self):
        """Setup test method."""
        self.client = HTTPClient("https://api.example.com")

    def test_unsupported_method(self):
        """Test unsupported HTTP method raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            self.client._make_request("PATCH", "/test")

        assert "Unsupported HTTP method: PATCH" in str(exc_info.value)
