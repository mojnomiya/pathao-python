"""Tests for main client class."""

import pytest
from unittest.mock import Mock, patch

from pathao.client import PathaoClient
from pathao.exceptions import ConfigurationError


class TestPathaoClient:
    """Test cases for PathaoClient."""

    def test_init_with_parameters(self):
        """Test client initialization with parameters."""
        client = PathaoClient(
            client_id="test_id",
            client_secret="test_secret",
            username="test_user",
            password="test_pass",
            environment="sandbox",
        )

        assert client.http_client.base_url == "https://courier-api-sandbox.pathao.com"
        assert hasattr(client, "stores")
        assert hasattr(client, "orders")
        assert hasattr(client, "locations")
        assert hasattr(client, "prices")

    def test_init_production_environment(self):
        """Test client initialization with production environment."""
        client = PathaoClient(
            client_id="test_id",
            client_secret="test_secret",
            username="test_user",
            password="test_pass",
            environment="production",
        )

        assert client.http_client.base_url == "https://courier-api.pathao.com"

    def test_init_invalid_environment(self):
        """Test client initialization with invalid environment."""
        with pytest.raises(ConfigurationError) as exc_info:
            PathaoClient(
                client_id="test_id",
                client_secret="test_secret",
                username="test_user",
                password="test_pass",
                environment="invalid",
            )
        assert "Invalid environment" in str(exc_info.value)

    @patch.dict(
        "os.environ",
        {
            "PATHAO_CLIENT_ID": "env_id",
            "PATHAO_CLIENT_SECRET": "env_secret",
            "PATHAO_USERNAME": "env_user",
            "PATHAO_PASSWORD": "env_pass",
        },
    )
    def test_init_with_environment_variables(self):
        """Test client initialization with environment variables."""
        client = PathaoClient()

        assert client.auth_module.credentials["client_id"] == "env_id"
        assert client.auth_module.credentials["username"] == "env_user"

    def test_init_missing_credentials(self):
        """Test client initialization with missing credentials."""
        with pytest.raises(ConfigurationError) as exc_info:
            PathaoClient()
        assert "Missing required credentials" in str(exc_info.value)

    def test_init_partial_credentials(self):
        """Test client initialization with partial credentials."""
        with pytest.raises(ConfigurationError) as exc_info:
            PathaoClient(client_id="test_id", username="test_user")
        assert "client_secret" in str(exc_info.value) or "password" in str(
            exc_info.value
        )

    def test_get_access_token(self):
        """Test get access token method."""
        client = PathaoClient(
            client_id="test_id",
            client_secret="test_secret",
            username="test_user",
            password="test_pass",
        )

        # Mock the auth module
        client.auth_module.get_access_token = Mock(return_value="test_token")

        token = client.get_access_token()
        assert token == "test_token"
        client.auth_module.get_access_token.assert_called_once()

    def test_refresh_token(self):
        """Test refresh token method."""
        client = PathaoClient(
            client_id="test_id",
            client_secret="test_secret",
            username="test_user",
            password="test_pass",
        )

        # Mock the auth module
        client.auth_module.refresh_token = Mock()

        client.refresh_token()
        client.auth_module.refresh_token.assert_called_once()

    def test_is_token_valid(self):
        """Test is token valid method."""
        client = PathaoClient(
            client_id="test_id",
            client_secret="test_secret",
            username="test_user",
            password="test_pass",
        )

        # Mock the auth module
        client.auth_module.is_token_valid = Mock(return_value=True)

        is_valid = client.is_token_valid()
        assert is_valid is True
        client.auth_module.is_token_valid.assert_called_once()

    def test_module_initialization(self):
        """Test that all modules are properly initialized."""
        client = PathaoClient(
            client_id="test_id",
            client_secret="test_secret",
            username="test_user",
            password="test_pass",
        )

        # Check that all modules are initialized with correct dependencies
        assert client.stores.http_client == client.http_client
        assert client.stores.auth_module == client.auth_module

        assert client.orders.http_client == client.http_client
        assert client.orders.auth_module == client.auth_module

        assert client.locations.http_client == client.http_client
        assert client.locations.auth_module == client.auth_module

        assert client.prices.http_client == client.http_client
        assert client.prices.auth_module == client.auth_module

    @patch.dict(
        "os.environ",
        {
            "PATHAO_CLIENT_ID": "env_id",
            "PATHAO_CLIENT_SECRET": "env_secret",
            "PATHAO_USERNAME": "env_user",
        },
    )
    def test_init_mixed_credentials(self):
        """Test client initialization with mixed credentials."""
        client = PathaoClient(password="param_pass")

        assert client.auth_module.credentials["client_id"] == "env_id"
        assert client.auth_module.credentials["password"] == "param_pass"

    def test_get_base_url_sandbox(self):
        """Test base URL for sandbox environment."""
        client = PathaoClient(
            client_id="test_id",
            client_secret="test_secret",
            username="test_user",
            password="test_pass",
        )
        url = client._get_base_url("sandbox")
        assert url == "https://courier-api-sandbox.pathao.com"

    def test_get_base_url_production(self):
        """Test base URL for production environment."""
        client = PathaoClient(
            client_id="test_id",
            client_secret="test_secret",
            username="test_user",
            password="test_pass",
        )
        url = client._get_base_url("production")
        assert url == "https://courier-api.pathao.com"
