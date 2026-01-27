"""HTTP client wrapper for Pathao Python SDK."""

import json
import time
from typing import Dict, Optional, Union
from urllib.parse import urljoin

import requests
from requests.exceptions import (
    ConnectionError,
    HTTPError,
    RequestException,
    Timeout,
)

from .exceptions import APIError, NetworkError
from .logger import get_logger

logger = get_logger(__name__)


class HTTPClient:
    """HTTP client wrapper with retry logic and error handling."""

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
        retry_backoff: float = 0.3,
    ):
        """Initialize HTTP client.

        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_backoff: Backoff factor for exponential backoff
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff
        self.session = requests.Session()

    def get(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Union[str, int]]] = None,
    ) -> dict:
        """Make GET request.

        Args:
            endpoint: API endpoint
            headers: Request headers
            params: Query parameters

        Returns:
            Response data as dictionary

        Raises:
            APIError: For API-related errors
            NetworkError: For network-related errors
        """
        return self._make_request("GET", endpoint, headers=headers, params=params)

    def post(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[dict] = None,
    ) -> dict:
        """Make POST request.

        Args:
            endpoint: API endpoint
            headers: Request headers
            data: Request payload

        Returns:
            Response data as dictionary

        Raises:
            APIError: For API-related errors
            NetworkError: For network-related errors
        """
        return self._make_request("POST", endpoint, headers=headers, data=data)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Union[str, int]]] = None,
        data: Optional[dict] = None,
    ) -> dict:
        """Make HTTP request with retry logic.

        Args:
            method: HTTP method
            endpoint: API endpoint
            headers: Request headers
            params: Query parameters
            data: Request payload

        Returns:
            Response data as dictionary

        Raises:
            APIError: For API-related errors
            NetworkError: For network-related errors
        """
        url = urljoin(f"{self.base_url}/", endpoint.lstrip("/"))
        headers = headers or {}
        headers.setdefault("Content-Type", "application/json")

        logger.debug(f"Making {method} request to {url}")

        for attempt in range(self.max_retries + 1):
            try:
                if method == "GET":
                    response = self.session.get(
                        url, headers=headers, params=params, timeout=self.timeout
                    )
                elif method == "POST":
                    json_data = json.dumps(data) if data else None
                    response = self.session.post(
                        url, headers=headers, data=json_data, timeout=self.timeout
                    )
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                # Check for HTTP errors
                response.raise_for_status()

                # Parse JSON response
                try:
                    response_data = response.json()
                    logger.debug(f"Request successful: {response.status_code}")
                    return response_data  # type: ignore[no-any-return]
                except json.JSONDecodeError as e:
                    raise APIError(
                        f"Invalid JSON response: {e}",
                        status_code=response.status_code,
                        response_data={"raw_response": response.text},
                    )

            except Timeout as e:
                if not self._should_retry(e, attempt):
                    raise NetworkError(f"Request timeout after {self.timeout}s")
                logger.warning(f"Request timeout, retrying... (attempt {attempt + 1})")

            except ConnectionError as e:
                if not self._should_retry(e, attempt):
                    raise NetworkError(f"Connection error: {e}")
                logger.warning(f"Connection error, retrying... (attempt {attempt + 1})")

            except HTTPError as e:
                response = e.response
                try:
                    error_data = response.json()
                except json.JSONDecodeError:
                    error_data = {"raw_response": response.text}

                # Don't retry client errors (4xx)
                if 400 <= response.status_code < 500:
                    raise APIError(
                        f"HTTP {response.status_code}: {response.reason}",
                        status_code=response.status_code,
                        response_data=error_data,
                    )

                # Retry server errors (5xx)
                if not self._should_retry(e, attempt):
                    raise APIError(
                        f"HTTP {response.status_code}: {response.reason}",
                        status_code=response.status_code,
                        response_data=error_data,
                    )
                logger.warning(
                    f"Server error {response.status_code}, retrying... "
                    f"(attempt {attempt + 1})"
                )

            except RequestException as e:
                if not self._should_retry(e, attempt):
                    raise NetworkError(f"Request failed: {e}")
                logger.warning(f"Request failed, retrying... (attempt {attempt + 1})")

            # Wait before retry
            if attempt < self.max_retries:
                self._exponential_backoff(attempt)

        # This should never be reached due to the exception handling above
        raise NetworkError("Maximum retries exceeded")

    def _should_retry(self, exception: Exception, attempt: int) -> bool:
        """Determine if request should be retried.

        Args:
            exception: Exception that occurred
            attempt: Current attempt number (0-based)

        Returns:
            True if should retry, False otherwise
        """
        if attempt >= self.max_retries:
            return False

        # Retry on network errors
        if isinstance(exception, (Timeout, ConnectionError)):
            return True

        # Retry on server errors (5xx)
        if isinstance(exception, HTTPError):
            return exception.response.status_code >= 500

        # Retry on general request exceptions
        if isinstance(exception, RequestException):
            return True

        return False

    def _exponential_backoff(self, attempt: int) -> None:
        """Wait with exponential backoff.

        Args:
            attempt: Current attempt number (0-based)
        """
        wait_time = self.retry_backoff * (2**attempt)
        logger.debug(f"Waiting {wait_time:.2f}s before retry")
        time.sleep(wait_time)
