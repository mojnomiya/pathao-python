"""Tests for order management module."""

import pytest
from unittest.mock import Mock

from pathao.exceptions import ValidationError, NotFoundError, APIError
from pathao.models import Order, OrderInfo, BulkOrderResponse
from pathao.modules.order import OrderModule


class TestOrderModule:
    """Test cases for OrderModule."""

    @pytest.fixture
    def mock_http_client(self):
        """Mock HTTP client."""
        return Mock()

    @pytest.fixture
    def mock_auth_module(self):
        """Mock auth module."""
        mock = Mock()
        mock.get_access_token.return_value = "test_token"
        return mock

    @pytest.fixture
    def order_module(self, mock_http_client, mock_auth_module):
        """Order module instance."""
        return OrderModule(mock_http_client, mock_auth_module)

    def test_init(self, mock_http_client, mock_auth_module):
        """Test order module initialization."""
        module = OrderModule(mock_http_client, mock_auth_module)
        assert module.http_client == mock_http_client
        assert module.auth_module == mock_auth_module

    def test_create_success(self, order_module, mock_http_client, mock_auth_module):
        """Test successful order creation."""
        # Mock response
        mock_response = {
            "data": {
                "data": {
                    "consignment_id": "CON123456",
                    "merchant_order_id": "ORDER001",
                    "order_status": "Pending",
                    "delivery_fee": 60.0,
                    "created_at": "2023-01-01T10:00:00Z",
                    "updated_at": "2023-01-01T10:00:00Z",
                }
            }
        }
        mock_http_client.post.return_value = mock_response

        # Call method
        order = order_module.create(
            store_id=1,
            merchant_order_id="ORDER001",
            recipient_name="John Doe",
            recipient_phone="01712345678",
            recipient_address="123 Test Street, Dhaka",
            recipient_city=1,
            recipient_zone=2,
            delivery_type=48,
            item_type=2,
            item_quantity=1,
            item_weight=0.5,
            amount_to_collect=100.0,
            item_description="Test item",
        )

        # Verify
        assert isinstance(order, Order)
        assert order.consignment_id == "CON123456"
        assert order.merchant_order_id == "ORDER001"
        assert order.delivery_fee == 60.0

        # Verify API call
        mock_auth_module.get_access_token.assert_called_once()
        mock_http_client.post.assert_called_once()

    def test_create_validation_errors(self, order_module):
        """Test order creation validation errors."""
        # Test invalid store_id
        with pytest.raises(ValueError) as exc_info:
            order_module.create(
                0,
                "ORDER001",
                "John",
                "01712345678",
                "123 Test St",
                1,
                2,
                48,
                2,
                1,
                0.5,
                0,
            )
        assert "store_id must be a positive integer" in str(exc_info.value)

        # Test empty merchant_order_id
        with pytest.raises(ValueError) as exc_info:
            order_module.create(
                1, "", "John", "01712345678", "123 Test St", 1, 2, 48, 2, 1, 0.5, 0
            )
        assert "merchant_order_id is required" in str(exc_info.value)

        # Test short recipient name
        with pytest.raises(ValidationError) as exc_info:
            order_module.create(
                1,
                "ORDER001",
                "Jo",
                "01712345678",
                "123 Test St",
                1,
                2,
                48,
                2,
                1,
                0.5,
                0,
            )
        assert "at least 3 characters" in str(exc_info.value)

        # Test invalid phone
        with pytest.raises(ValidationError) as exc_info:
            order_module.create(
                1, "ORDER001", "John", "123", "123 Test St", 1, 2, 48, 2, 1, 0.5, 0
            )
        assert "exactly 11 digits" in str(exc_info.value)

        # Test invalid delivery type
        with pytest.raises(ValidationError) as exc_info:
            order_module.create(
                1,
                "ORDER001",
                "John",
                "01712345678",
                "123 Test St",
                1,
                2,
                99,
                2,
                1,
                0.5,
                0,
            )
        assert "must be 12 (OnDemand) or 48 (Normal)" in str(exc_info.value)

        # Test negative amount
        with pytest.raises(ValueError) as exc_info:
            order_module.create(
                1,
                "ORDER001",
                "John",
                "01712345678",
                "123 Test St",
                1,
                2,
                48,
                2,
                1,
                0.5,
                -10,
            )
        assert "amount_to_collect must be non-negative" in str(exc_info.value)

    def test_create_bulk_success(
        self, order_module, mock_http_client, mock_auth_module
    ):
        """Test successful bulk order creation."""
        # Mock response
        mock_response = {
            "code": 202,
            "message": "Orders submitted for processing",
            "data": {"batch_id": "BATCH123"},
        }
        mock_http_client.post.return_value = mock_response

        # Prepare orders
        orders = [
            {
                "store_id": 1,
                "merchant_order_id": "ORDER001",
                "recipient_name": "John Doe",
                "recipient_phone": "01712345678",
                "recipient_address": "123 Test Street",
                "recipient_city": 1,
                "recipient_zone": 2,
                "delivery_type": 48,
                "item_type": 2,
                "item_quantity": 1,
                "item_weight": 0.5,
                "amount_to_collect": 100.0,
            }
        ]

        # Call method
        response = order_module.create_bulk(orders)

        # Verify
        assert isinstance(response, BulkOrderResponse)
        assert response.code == 202
        assert response.message == "Orders submitted for processing"
        assert response.data["batch_id"] == "BATCH123"

        # Verify API call
        mock_auth_module.get_access_token.assert_called_once()
        # The order should include item_description field
        expected_order = orders[0].copy()
        expected_order["item_description"] = ""
        mock_http_client.post.assert_called_once_with(
            "aladdin/api/v1/orders/bulk",
            {"Authorization": "Bearer test_token"},
            {"orders": [expected_order]},
        )

    def test_create_bulk_validation_errors(self, order_module):
        """Test bulk order validation errors."""
        # Test empty orders list
        with pytest.raises(ValueError) as exc_info:
            order_module.create_bulk([])
        assert "orders must be a non-empty list" in str(exc_info.value)

        # Test invalid order in list
        orders = [
            {
                "store_id": 0,  # Invalid
                "merchant_order_id": "ORDER001",
                "recipient_name": "John",
                "recipient_phone": "01712345678",
                "recipient_address": "123 Test Street",
                "recipient_city": 1,
                "recipient_zone": 2,
                "delivery_type": 48,
                "item_type": 2,
                "item_quantity": 1,
                "item_weight": 0.5,
                "amount_to_collect": 0,
            }
        ]
        with pytest.raises(ValueError) as exc_info:
            order_module.create_bulk(orders)
        assert "Order 0:" in str(exc_info.value)
        assert "store_id must be a positive integer" in str(exc_info.value)

    def test_get_info_success(self, order_module, mock_http_client, mock_auth_module):
        """Test successful order info retrieval."""
        # Mock response
        mock_response = {
            "data": {
                "consignment_id": "CON123456",
                "merchant_order_id": "ORDER001",
                "order_status": "Delivered",
                "order_status_slug": "delivered",
                "updated_at": "2023-01-02T15:30:00Z",
                "invoice_id": "INV789",
            }
        }
        mock_http_client.get.return_value = mock_response

        # Call method
        order_info = order_module.get_info("CON123456")

        # Verify
        assert isinstance(order_info, OrderInfo)
        assert order_info.consignment_id == "CON123456"
        assert order_info.order_status == "Delivered"
        assert order_info.invoice_id == "INV789"

        # Verify API call
        mock_auth_module.get_access_token.assert_called_once()
        mock_http_client.get.assert_called_once_with(
            "aladdin/api/v1/orders/CON123456/info",
            {"Authorization": "Bearer test_token"},
        )

    def test_get_info_validation_error(self, order_module):
        """Test order info validation error."""
        with pytest.raises(ValueError) as exc_info:
            order_module.get_info("")
        assert "consignment_id is required" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            order_module.get_info(None)
        assert "consignment_id is required" in str(exc_info.value)

    def test_get_info_not_found(self, order_module, mock_http_client):
        """Test order not found error."""
        mock_http_client.get.side_effect = Exception("404 Not Found")

        with pytest.raises(NotFoundError) as exc_info:
            order_module.get_info("INVALID123")
        assert "Order with identifier 'INVALID123' not found" in str(exc_info.value)

    def test_create_api_error(self, order_module, mock_http_client):
        """Test API error during order creation."""
        mock_http_client.post.side_effect = APIError("Bad request", 400)

        with pytest.raises(APIError):
            order_module.create(
                1,
                "ORDER001",
                "John Doe",
                "01712345678",
                "123 Test Street",
                1,
                2,
                48,
                2,
                1,
                0.5,
                0,
            )

    def test_create_bulk_api_error(self, order_module, mock_http_client):
        """Test API error during bulk order creation."""
        mock_http_client.post.side_effect = APIError("Server error", 500)

        orders = [
            {
                "store_id": 1,
                "merchant_order_id": "ORDER001",
                "recipient_name": "John Doe",
                "recipient_phone": "01712345678",
                "recipient_address": "123 Test Street",
                "recipient_city": 1,
                "recipient_zone": 2,
                "delivery_type": 48,
                "item_type": 2,
                "item_quantity": 1,
                "item_weight": 0.5,
                "amount_to_collect": 0,
            }
        ]

        with pytest.raises(APIError):
            order_module.create_bulk(orders)

    def test_get_info_api_error(self, order_module, mock_http_client):
        """Test API error during order info retrieval."""
        mock_http_client.get.side_effect = APIError("Server error", 500)

        with pytest.raises(APIError):
            order_module.get_info("CON123456")
