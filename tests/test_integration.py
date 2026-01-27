"""Integration tests for Pathao Python SDK."""

import pytest
from unittest.mock import Mock, patch
from pathao import PathaoClient
from pathao.exceptions import AuthenticationError, ValidationError, APIError
from tests.fixtures.mock_responses import (
    AUTH_SUCCESS_RESPONSE,
    STORE_CREATE_SUCCESS,
    ORDER_CREATE_SUCCESS,
    CITIES_SUCCESS,
    PRICE_SUCCESS,
)


class TestPathaoClientIntegration:
    """Integration tests for PathaoClient with all modules."""

    @pytest.fixture
    def client(self):
        """Create a PathaoClient instance for testing."""
        return PathaoClient(
            client_id="test_client_id",
            client_secret="test_client_secret",
            username="test@example.com",
            password="test_password",
            environment="sandbox",
        )

    @patch("pathao.http_client.HTTPClient.post")
    def test_full_workflow_create_store_and_order(self, mock_post, client):
        """Test full workflow: authenticate, create store, create order."""
        # Mock authentication
        mock_post.side_effect = [
            AUTH_SUCCESS_RESPONSE,  # Initial auth
            STORE_CREATE_SUCCESS,  # Store creation
            ORDER_CREATE_SUCCESS,  # Order creation
        ]

        # Create store
        store = client.stores.create(
            store_name="Integration Test Store",
            contact_name="John Doe",
            contact_number="01712345678",
            address="123 Test Street, Dhaka",
            city_id=1,
            zone_id=1,
            area_id=1,
        )

        assert store.store_id == 123
        assert store.store_name == "Test Store"

        # Create order
        order = client.orders.create(
            store_id=123,
            merchant_order_id="TEST-001",
            recipient_name="Jane Doe",
            recipient_phone="01712345678",
            recipient_address="456 Test Road, Dhaka",
            recipient_city=1,
            recipient_zone=1,
            delivery_type=48,
            item_type=2,
            item_quantity=1,
            item_weight=0.5,
            amount_to_collect=100.0,
        )

        assert order.consignment_id == "D-12345"
        assert order.order_status == "Pending"

    @patch("pathao.http_client.HTTPClient.get")
    @patch("pathao.http_client.HTTPClient.post")
    def test_location_and_price_workflow(self, mock_post, mock_get, client):
        """Test location lookup and price calculation workflow."""
        # Mock authentication and API calls
        mock_post.side_effect = [
            AUTH_SUCCESS_RESPONSE,  # Initial auth
            PRICE_SUCCESS,  # Price calculation
        ]
        mock_get.return_value = CITIES_SUCCESS

        # Get cities
        cities = client.locations.get_cities()
        assert len(cities.data) == 3
        assert cities.data[0].city_name == "Dhaka"

        # Calculate price
        price = client.prices.calculate(
            store_id=1,
            delivery_type=48,
            item_type=2,
            weight=0.5,
            recipient_city=1,
            recipient_zone=1,
        )

        assert price.price == 60.0
        assert price.final_price == 55.0
        assert price.cod_enabled is True

    @patch("pathao.http_client.HTTPClient.post")
    def test_authentication_error_propagation(self, mock_post, client):
        """Test that authentication errors propagate correctly across modules."""
        # Mock authentication failure
        mock_post.side_effect = AuthenticationError("Invalid credentials")

        # Any module operation should fail with authentication error
        with pytest.raises(AuthenticationError):
            client.stores.list()

        with pytest.raises(AuthenticationError):
            client.orders.create(
                store_id=1,
                merchant_order_id="TEST-001",
                recipient_name="Test",
                recipient_phone="01712345678",
                recipient_address="Test Address",
                recipient_city=1,
                recipient_zone=1,
                delivery_type=48,
                item_type=2,
                item_quantity=1,
                item_weight=0.5,
                amount_to_collect=0,
            )

    def test_validation_error_consistency(self, client):
        """Test that validation errors are consistent across modules."""
        # Test invalid phone number validation across modules
        with pytest.raises(ValidationError, match="Invalid phone number"):
            client.stores.create(
                store_name="Test Store",
                contact_name="John Doe",
                contact_number="invalid_phone",  # Invalid phone
                address="123 Test Street",
                city_id=1,
                zone_id=1,
                area_id=1,
            )

        with pytest.raises(ValidationError, match="Invalid phone number"):
            client.orders.create(
                store_id=1,
                merchant_order_id="TEST-001",
                recipient_name="Test",
                recipient_phone="invalid_phone",  # Invalid phone
                recipient_address="Test Address",
                recipient_city=1,
                recipient_zone=1,
                delivery_type=48,
                item_type=2,
                item_quantity=1,
                item_weight=0.5,
                amount_to_collect=0,
            )

    @patch("pathao.http_client.HTTPClient.post")
    def test_token_refresh_across_modules(self, mock_post, client):
        """Test that token refresh works across different module operations."""
        # Mock initial auth and refresh
        mock_post.side_effect = [
            AUTH_SUCCESS_RESPONSE,  # Initial auth
            AUTH_SUCCESS_RESPONSE,  # Token refresh
            STORE_CREATE_SUCCESS,  # Store creation after refresh
        ]

        # Simulate token expiring soon
        client.auth._token.created_at = client.auth._token.created_at.replace(
            year=2020  # Make token very old
        )

        # This should trigger token refresh
        store = client.stores.create(
            store_name="Test Store",
            contact_name="John Doe",
            contact_number="01712345678",
            address="123 Test Street",
            city_id=1,
            zone_id=1,
            area_id=1,
        )

        assert store.store_id == 123
        # Verify that post was called 3 times (auth + refresh + create)
        assert mock_post.call_count == 3

    def test_module_dependency_injection(self, client):
        """Test that all modules receive proper dependencies."""
        # Verify all modules are initialized
        assert client.stores is not None
        assert client.orders is not None
        assert client.locations is not None
        assert client.prices is not None

        # Verify modules have access to HTTP client and auth
        assert client.stores.http_client is not None
        assert client.stores.auth_module is not None
        assert client.orders.http_client is not None
        assert client.orders.auth_module is not None
        assert client.locations.http_client is not None
        assert client.locations.auth_module is not None
        assert client.prices.http_client is not None
        assert client.prices.auth_module is not None

        # Verify all modules share the same instances
        assert client.stores.http_client is client.orders.http_client
        assert client.stores.auth_module is client.orders.auth_module


class TestErrorHandlingIntegration:
    """Integration tests for error handling across modules."""

    @pytest.fixture
    def client(self):
        """Create a PathaoClient instance for testing."""
        return PathaoClient(
            client_id="test_client_id",
            client_secret="test_client_secret",
            username="test@example.com",
            password="test_password",
            environment="sandbox",
        )

    @patch("pathao.http_client.HTTPClient.post")
    def test_api_error_consistency(self, mock_post, client):
        """Test that API errors are handled consistently across modules."""
        # Mock API error response
        mock_post.side_effect = APIError("Server error", status_code=500)

        # All modules should handle API errors the same way
        with pytest.raises(APIError):
            client.stores.create(
                store_name="Test Store",
                contact_name="John Doe",
                contact_number="01712345678",
                address="123 Test Street",
                city_id=1,
                zone_id=1,
                area_id=1,
            )

        with pytest.raises(APIError):
            client.orders.create(
                store_id=1,
                merchant_order_id="TEST-001",
                recipient_name="Test",
                recipient_phone="01712345678",
                recipient_address="Test Address",
                recipient_city=1,
                recipient_zone=1,
                delivery_type=48,
                item_type=2,
                item_quantity=1,
                item_weight=0.5,
                amount_to_collect=0,
            )

    def test_environment_configuration_consistency(self):
        """Test that environment configuration is consistent across all modules."""
        # Test sandbox environment
        sandbox_client = PathaoClient(
            client_id="test_client_id",
            client_secret="test_client_secret",
            username="test@example.com",
            password="test_password",
            environment="sandbox",
        )

        assert "sandbox" in sandbox_client.http_client.base_url

        # Test production environment
        prod_client = PathaoClient(
            client_id="test_client_id",
            client_secret="test_client_secret",
            username="test@example.com",
            password="test_password",
            environment="production",
        )

        assert "api.pathao.com" in prod_client.http_client.base_url
