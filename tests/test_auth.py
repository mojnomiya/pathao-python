"""Tests for Pathao SDK authentication module."""

from datetime import datetime, timedelta
from unittest.mock import Mock
import pytest

from pathao.modules.auth import AuthModule
from pathao.models import AuthToken
from pathao.exceptions import AuthenticationError, APIError, NetworkError


class TestAuthModuleInitialization:
    """Test AuthModule initialization."""

    def test_init_success(self):
        """Test successful initialization."""
        http_client = Mock()
        credentials = {
            "client_id": "test_id",
            "client_secret": "test_secret",
            "username": "test@example.com",
            "password": "password123",
        }

        auth = AuthModule(http_client, credentials)

        assert auth.http_client == http_client
        assert auth.credentials == credentials
        assert auth._token is None

    def test_init_missing_credentials(self):
        """Test initialization with missing credentials."""
        http_client = Mock()
        credentials = {
            "client_id": "test_id",
            # Missing client_secret, username, password
        }

        with pytest.raises(AuthenticationError) as exc_info:
            AuthModule(http_client, credentials)

        assert "Missing required credentials" in str(exc_info.value)
        assert "client_secret" in str(exc_info.value)

    def test_init_empty_credentials(self):
        """Test initialization with empty credential values."""
        http_client = Mock()
        credentials = {
            "client_id": "",
            "client_secret": "test_secret",
            "username": "test@example.com",
            "password": "password123",
        }

        with pytest.raises(AuthenticationError) as exc_info:
            AuthModule(http_client, credentials)

        assert "Missing required credentials: client_id" in str(exc_info.value)


class TestAuthModuleTokenValidation:
    """Test AuthModule token validation methods."""

    def setup_method(self):
        """Setup test method."""
        self.http_client = Mock()
        self.credentials = {
            "client_id": "test_id",
            "client_secret": "test_secret",
            "username": "test@example.com",
            "password": "password123",
        }
        self.auth = AuthModule(self.http_client, self.credentials)

    def test_is_token_valid_no_token(self):
        """Test token validation with no token."""
        assert self.auth.is_token_valid() is False

    def test_is_token_valid_expired_token(self):
        """Test token validation with expired token."""
        expired_token = AuthToken(
            access_token="token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="refresh",
            created_at=datetime.now() - timedelta(hours=2),
        )
        self.auth._token = expired_token

        assert self.auth.is_token_valid() is False

    def test_is_token_valid_valid_token(self):
        """Test token validation with valid token."""
        valid_token = AuthToken(
            access_token="token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="refresh",
            created_at=datetime.now(),
        )
        self.auth._token = valid_token

        assert self.auth.is_token_valid() is True

    def test_is_token_expiring_soon_no_token(self):
        """Test expiring soon check with no token."""
        assert self.auth.is_token_expiring_soon() is True

    def test_is_token_expiring_soon_true(self):
        """Test expiring soon check returns True."""
        expiring_token = AuthToken(
            access_token="token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="refresh",
            created_at=datetime.now() - timedelta(minutes=58),  # Expires in 2 minutes
        )
        self.auth._token = expiring_token

        assert self.auth.is_token_expiring_soon(300) is True  # 5 minutes

    def test_is_token_expiring_soon_false(self):
        """Test expiring soon check returns False."""
        fresh_token = AuthToken(
            access_token="token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="refresh",
            created_at=datetime.now(),
        )
        self.auth._token = fresh_token

        assert self.auth.is_token_expiring_soon(300) is False


class TestAuthModuleTokenIssuance:
    """Test AuthModule token issuance."""

    def setup_method(self):
        """Setup test method."""
        self.http_client = Mock()
        self.credentials = {
            "client_id": "test_id",
            "client_secret": "test_secret",
            "username": "test@example.com",
            "password": "password123",
        }
        self.auth = AuthModule(self.http_client, self.credentials)

    def test_issue_token_password_grant_success(self):
        """Test successful password grant token issuance."""
        mock_response = {
            "access_token": "new_access_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "new_refresh_token",
        }
        self.http_client.post.return_value = mock_response

        token = self.auth._issue_token("password")

        assert token.access_token == "new_access_token"
        assert token.token_type == "Bearer"
        assert token.expires_in == 3600
        assert token.refresh_token == "new_refresh_token"
        assert isinstance(token.created_at, datetime)

        self.http_client.post.assert_called_once_with(
            "aladdin/api/v1/issue-token",
            data={
                "client_id": "test_id",
                "client_secret": "test_secret",
                "username": "test@example.com",
                "password": "password123",
                "grant_type": "password",
            },
        )

    def test_issue_token_refresh_grant_success(self):
        """Test successful refresh token grant."""
        # Set existing token
        existing_token = AuthToken(
            access_token="old_token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="old_refresh_token",
            created_at=datetime.now(),
        )
        self.auth._token = existing_token

        mock_response = {
            "access_token": "new_access_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "new_refresh_token",
        }
        self.http_client.post.return_value = mock_response

        token = self.auth._issue_token("refresh_token")

        assert token.access_token == "new_access_token"
        assert token.refresh_token == "new_refresh_token"

        self.http_client.post.assert_called_once_with(
            "aladdin/api/v1/issue-token",
            data={
                "client_id": "test_id",
                "client_secret": "test_secret",
                "refresh_token": "old_refresh_token",
                "grant_type": "refresh_token",
            },
        )

    def test_issue_token_refresh_grant_no_refresh_token(self):
        """Test refresh token grant with no refresh token."""
        with pytest.raises(AuthenticationError) as exc_info:
            self.auth._issue_token("refresh_token")

        assert "No refresh token available" in str(exc_info.value)

    def test_issue_token_unsupported_grant_type(self):
        """Test unsupported grant type."""
        with pytest.raises(AuthenticationError) as exc_info:
            self.auth._issue_token("client_credentials")

        assert "Unsupported grant type: client_credentials" in str(exc_info.value)

    def test_issue_token_api_error(self):
        """Test token issuance with API error."""
        self.http_client.post.side_effect = APIError(
            "Invalid credentials", status_code=401
        )

        with pytest.raises(AuthenticationError) as exc_info:
            self.auth._issue_token("password")

        assert "Token request failed" in str(exc_info.value)

    def test_issue_token_network_error(self):
        """Test token issuance with network error."""
        self.http_client.post.side_effect = NetworkError("Connection failed")

        with pytest.raises(AuthenticationError) as exc_info:
            self.auth._issue_token("password")

        assert "Token request failed" in str(exc_info.value)

    def test_issue_token_missing_response_fields(self):
        """Test token issuance with missing response fields."""
        mock_response = {
            "access_token": "token",
            # Missing expires_in and refresh_token
        }
        self.http_client.post.return_value = mock_response

        with pytest.raises(AuthenticationError) as exc_info:
            self.auth._issue_token("password")

        assert "Token request failed" in str(exc_info.value)


class TestAuthModuleGetAccessToken:
    """Test AuthModule get_access_token method."""

    def setup_method(self):
        """Setup test method."""
        self.http_client = Mock()
        self.credentials = {
            "client_id": "test_id",
            "client_secret": "test_secret",
            "username": "test@example.com",
            "password": "password123",
        }
        self.auth = AuthModule(self.http_client, self.credentials)

    def test_get_access_token_no_token(self):
        """Test get access token with no existing token."""
        mock_response = {
            "access_token": "new_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "refresh_token",
        }
        self.http_client.post.return_value = mock_response

        token = self.auth.get_access_token()

        assert token == "new_token"
        assert self.auth._token.access_token == "new_token"

    def test_get_access_token_valid_token(self):
        """Test get access token with valid existing token."""
        valid_token = AuthToken(
            access_token="existing_token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="refresh_token",
            created_at=datetime.now(),
        )
        self.auth._token = valid_token

        token = self.auth.get_access_token()

        assert token == "existing_token"
        # Should not make HTTP request
        self.http_client.post.assert_not_called()

    def test_get_access_token_expiring_soon_refresh_success(self):
        """Test get access token with expiring token, successful refresh."""
        expiring_token = AuthToken(
            access_token="old_token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="old_refresh",
            created_at=datetime.now() - timedelta(minutes=58),
        )
        self.auth._token = expiring_token

        mock_response = {
            "access_token": "refreshed_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "new_refresh",
        }
        self.http_client.post.return_value = mock_response

        token = self.auth.get_access_token()

        assert token == "refreshed_token"
        # Should use refresh token grant
        self.http_client.post.assert_called_once()
        call_args = self.http_client.post.call_args[1]["data"]
        assert call_args["grant_type"] == "refresh_token"

    def test_get_access_token_expiring_soon_refresh_fails(self):
        """Test get access token with expiring token, refresh fails."""
        expiring_token = AuthToken(
            access_token="old_token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="old_refresh",
            created_at=datetime.now() - timedelta(minutes=58),
        )
        self.auth._token = expiring_token

        # First call (refresh) fails, second call (password) succeeds
        self.http_client.post.side_effect = [
            AuthenticationError("Refresh failed"),
            {
                "access_token": "new_token",
                "token_type": "Bearer",
                "expires_in": 3600,
                "refresh_token": "new_refresh",
            },
        ]

        token = self.auth.get_access_token()

        assert token == "new_token"
        assert self.http_client.post.call_count == 2


class TestAuthModuleRefreshToken:
    """Test AuthModule refresh_token method."""

    def setup_method(self):
        """Setup test method."""
        self.http_client = Mock()
        self.credentials = {
            "client_id": "test_id",
            "client_secret": "test_secret",
            "username": "test@example.com",
            "password": "password123",
        }
        self.auth = AuthModule(self.http_client, self.credentials)

    def test_refresh_token_success(self):
        """Test successful manual token refresh."""
        existing_token = AuthToken(
            access_token="old_token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="old_refresh",
            created_at=datetime.now(),
        )
        self.auth._token = existing_token

        mock_response = {
            "access_token": "refreshed_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "new_refresh",
        }
        self.http_client.post.return_value = mock_response

        new_token = self.auth.refresh_token()

        assert new_token.access_token == "refreshed_token"
        assert new_token.refresh_token == "new_refresh"
        assert self.auth._token == new_token

    def test_refresh_token_no_token(self):
        """Test manual refresh with no existing token."""
        with pytest.raises(AuthenticationError) as exc_info:
            self.auth.refresh_token()

        assert "No refresh token available" in str(exc_info.value)

    def test_refresh_token_no_refresh_token(self):
        """Test manual refresh with token but no refresh token."""
        token_without_refresh = AuthToken(
            access_token="token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="",  # Empty refresh token
            created_at=datetime.now(),
        )
        self.auth._token = token_without_refresh

        with pytest.raises(AuthenticationError) as exc_info:
            self.auth.refresh_token()

        assert "No refresh token available" in str(exc_info.value)


class TestAuthModuleTokenStorage:
    """Test AuthModule token storage methods."""

    def setup_method(self):
        """Setup test method."""
        self.http_client = Mock()
        self.credentials = {
            "client_id": "test_id",
            "client_secret": "test_secret",
            "username": "test@example.com",
            "password": "password123",
        }
        self.auth = AuthModule(self.http_client, self.credentials)

    def test_store_and_load_token(self):
        """Test token storage and loading."""
        token = AuthToken(
            access_token="test_token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="refresh_token",
            created_at=datetime.now(),
        )

        self.auth._store_token(token)
        loaded_token = self.auth._load_token()

        assert loaded_token == token
        assert loaded_token.access_token == "test_token"

    def test_load_token_none(self):
        """Test loading token when none is stored."""
        loaded_token = self.auth._load_token()
        assert loaded_token is None
