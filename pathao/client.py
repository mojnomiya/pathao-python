"""Main client class for Pathao Python SDK."""

import os
from typing import Optional

from .exceptions import ConfigurationError
from .http_client import HTTPClient
from .modules.auth import AuthModule
from .modules.store import StoreModule
from .modules.order import OrderModule
from .modules.location import LocationModule
from .modules.price import PriceModule


class PathaoClient:
    """Main client for Pathao API."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        environment: str = "sandbox",
    ):
        """Initialize Pathao client."""
        # Load credentials
        credentials = self._load_credentials(
            client_id, client_secret, username, password
        )

        # Validate environment
        if environment not in ["sandbox", "production"]:
            raise ConfigurationError(
                "Invalid environment. Must be 'sandbox' or 'production'",
                missing_config="environment",
            )

        # Set base URL
        base_url = (
            "https://courier-api.pathao.com"
            if environment == "production"
            else "https://courier-api-sandbox.pathao.com"
        )

        # Initialize HTTP client
        self.http_client = HTTPClient(base_url)

        # Initialize auth module
        self.auth_module = AuthModule(self.http_client, credentials)

        # Initialize service modules
        self.stores = StoreModule(self.http_client, self.auth_module)
        self.orders = OrderModule(self.http_client, self.auth_module)
        self.locations = LocationModule(self.http_client, self.auth_module)
        self.prices = PriceModule(self.http_client, self.auth_module)

    def _load_credentials(
        self,
        client_id: Optional[str],
        client_secret: Optional[str],
        username: Optional[str],
        password: Optional[str],
    ) -> dict:
        """Load credentials from parameters or environment."""
        # Try parameters first, then environment variables
        credentials = {
            "client_id": client_id or os.getenv("PATHAO_CLIENT_ID"),
            "client_secret": client_secret or os.getenv("PATHAO_CLIENT_SECRET"),
            "username": username or os.getenv("PATHAO_USERNAME"),
            "password": password or os.getenv("PATHAO_PASSWORD"),
        }

        # Validate required credentials
        missing = [k for k, v in credentials.items() if not v]
        if missing:
            raise ConfigurationError(
                f"Missing required credentials: {', '.join(missing)}",
                missing_config=missing[0],
            )

        return credentials

    def get_access_token(self) -> str:
        """Get current access token."""
        return self.auth_module.get_access_token()

    def refresh_token(self) -> None:
        """Refresh access token."""
        self.auth_module.refresh_token()

    def is_token_valid(self) -> bool:
        """Check if current token is valid."""
        return self.auth_module.is_token_valid()
