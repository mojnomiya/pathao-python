"""Authentication module for Pathao Python SDK."""

from datetime import datetime
from typing import Dict, Optional

from ..exceptions import AuthenticationError
from ..http_client import HTTPClient
from ..logger import get_logger
from ..models import AuthToken

logger = get_logger(__name__)


class AuthModule:
    """Handles OAuth 2.0 authentication and token management."""

    def __init__(self, http_client: HTTPClient, credentials: Dict[str, str]):
        """Initialize authentication module.

        Args:
            http_client: HTTP client instance
            credentials: Dictionary containing client_id, client_secret,
                username, password

        Raises:
            AuthenticationError: If credentials are invalid
        """
        self.http_client = http_client
        self.credentials = credentials
        self._token: Optional[AuthToken] = None

        # Validate required credentials
        required_fields = ["client_id", "client_secret", "username", "password"]
        missing_fields = [
            field for field in required_fields if not credentials.get(field)
        ]
        if missing_fields:
            raise AuthenticationError(
                f"Missing required credentials: {', '.join(missing_fields)}"
            )

        logger.debug("AuthModule initialized")

    def get_access_token(self) -> str:
        """Get valid access token, refreshing if necessary.

        Returns:
            Valid access token string

        Raises:
            AuthenticationError: If authentication fails
        """
        if not self.is_token_valid():
            logger.debug("Token invalid or missing, obtaining new token")
            self._token = self._issue_token("password")
        elif self.is_token_expiring_soon():
            logger.debug("Token expiring soon, refreshing")
            try:
                self._token = self._issue_token("refresh_token")
            except AuthenticationError:
                logger.warning("Token refresh failed, obtaining new token")
                self._token = self._issue_token("password")

        assert self._token is not None  # Type hint for mypy
        return self._token.access_token

    def refresh_token(self) -> AuthToken:
        """Manually refresh the access token.

        Returns:
            New AuthToken object

        Raises:
            AuthenticationError: If token refresh fails
        """
        if not self._token or not self._token.refresh_token:
            raise AuthenticationError("No refresh token available")

        logger.debug("Manually refreshing token")
        self._token = self._issue_token("refresh_token")
        return self._token

    def is_token_valid(self) -> bool:
        """Check if current token is valid and not expired.

        Returns:
            True if token is valid, False otherwise
        """
        if not self._token:
            return False
        return not self._token.is_expired()

    def is_token_expiring_soon(self, seconds: int = 300) -> bool:
        """Check if token will expire within N seconds.

        Args:
            seconds: Number of seconds to check ahead

        Returns:
            True if token will expire soon, False otherwise
        """
        if not self._token:
            return True
        return self._token.will_expire_soon(seconds)

    def _issue_token(self, grant_type: str, **kwargs) -> AuthToken:
        """Issue or refresh access token.

        Args:
            grant_type: OAuth 2.0 grant type ('password' or 'refresh_token')
            **kwargs: Additional parameters

        Returns:
            New AuthToken object

        Raises:
            AuthenticationError: If token request fails
        """
        if grant_type == "password":
            payload = {
                "client_id": self.credentials["client_id"],
                "client_secret": self.credentials["client_secret"],
                "username": self.credentials["username"],
                "password": self.credentials["password"],
                "grant_type": "password",
            }
        elif grant_type == "refresh_token":
            if not self._token or not self._token.refresh_token:
                raise AuthenticationError("No refresh token available")
            payload = {
                "client_id": self.credentials["client_id"],
                "client_secret": self.credentials["client_secret"],
                "refresh_token": self._token.refresh_token,
                "grant_type": "refresh_token",
            }
        else:
            raise AuthenticationError(f"Unsupported grant type: {grant_type}")

        # Add any additional parameters
        payload.update(kwargs)

        try:
            logger.debug(f"Requesting token with grant_type: {grant_type}")
            response = self.http_client.post("aladdin/api/v1/issue-token", data=payload)

            # Parse response and create AuthToken
            token = AuthToken(
                access_token=response["access_token"],
                token_type=response.get("token_type", "Bearer"),
                expires_in=response["expires_in"],
                refresh_token=response["refresh_token"],
                created_at=datetime.now(),
            )

            logger.info(f"Token obtained successfully, expires in {token.expires_in}s")
            return token

        except Exception as e:
            error_msg = f"Token request failed: {e}"
            logger.error(error_msg)
            raise AuthenticationError(error_msg) from e

    def _store_token(self, token: AuthToken) -> None:
        """Store token in memory.

        Args:
            token: AuthToken to store
        """
        self._token = token
        logger.debug("Token stored in memory")

    def _load_token(self) -> Optional[AuthToken]:
        """Load token from memory.

        Returns:
            Stored AuthToken or None if not available
        """
        return self._token
