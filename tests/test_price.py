"""Tests for price calculation module."""

import pytest
from unittest.mock import Mock

from pathao.exceptions import ValidationError, APIError
from pathao.models import PriceDetails
from pathao.modules.price import PriceModule


class TestPriceModule:
    """Test cases for PriceModule."""

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
    def price_module(self, mock_http_client, mock_auth_module):
        """Price module instance."""
        return PriceModule(mock_http_client, mock_auth_module)

    def test_init(self, mock_http_client, mock_auth_module):
        """Test price module initialization."""
        module = PriceModule(mock_http_client, mock_auth_module)
        assert module.http_client == mock_http_client
        assert module.auth_module == mock_auth_module

    def test_calculate_success(self, price_module, mock_http_client, mock_auth_module):
        """Test successful price calculation."""
        mock_response = {
            "data": {
                "price": 60.0,
                "discount": 5.0,
                "promo_discount": 0.0,
                "plan_id": 1,
                "cod_enabled": True,
                "cod_percentage": 1.0,
                "additional_charge": 0.0,
                "final_price": 55.0,
            }
        }
        mock_http_client.post.return_value = mock_response

        price = price_module.calculate(
            store_id=1,
            item_type=2,
            delivery_type=48,
            item_weight=0.5,
            recipient_city=1,
            recipient_zone=2,
        )

        assert isinstance(price, PriceDetails)
        assert price.price == 60.0
        assert price.discount == 5.0
        assert price.final_price == 55.0
        assert price.cod_enabled is True

        mock_auth_module.get_access_token.assert_called_once()
        mock_http_client.post.assert_called_once_with(
            "aladdin/api/v1/merchant/price-plan",
            {"Authorization": "Bearer test_token"},
            {
                "store_id": 1,
                "item_type": 2,
                "delivery_type": 48,
                "item_weight": 0.5,
                "recipient_city": 1,
                "recipient_zone": 2,
            },
        )

    def test_calculate_validation_errors(self, price_module):
        """Test price calculation validation errors."""
        # Test invalid store_id
        with pytest.raises(ValueError) as exc_info:
            price_module.calculate(0, 2, 48, 0.5, 1, 2)
        assert "store_id must be a positive integer" in str(exc_info.value)

        # Test invalid item_type
        with pytest.raises(ValidationError) as exc_info:
            price_module.calculate(1, 99, 48, 0.5, 1, 2)
        assert "must be 1 (Document) or 2 (Parcel)" in str(exc_info.value)

        # Test invalid delivery_type
        with pytest.raises(ValidationError) as exc_info:
            price_module.calculate(1, 2, 99, 0.5, 1, 2)
        assert "must be 12 (OnDemand) or 48 (Normal)" in str(exc_info.value)

        # Test invalid weight
        with pytest.raises(ValidationError) as exc_info:
            price_module.calculate(1, 2, 48, 0.1, 1, 2)
        assert "must be at least 0.5 kg" in str(exc_info.value)

        # Test invalid recipient_city
        with pytest.raises(ValueError) as exc_info:
            price_module.calculate(1, 2, 48, 0.5, 0, 2)
        assert "recipient_city must be a positive integer" in str(exc_info.value)

        # Test invalid recipient_zone
        with pytest.raises(ValueError) as exc_info:
            price_module.calculate(1, 2, 48, 0.5, 1, 0)
        assert "recipient_zone must be a positive integer" in str(exc_info.value)

    def test_calculate_different_delivery_types(self, price_module, mock_http_client):
        """Test price calculation with different delivery types."""
        mock_response = {
            "data": {
                "price": 120.0,
                "discount": 0.0,
                "promo_discount": 10.0,
                "plan_id": 2,
                "cod_enabled": False,
                "cod_percentage": 0.0,
                "additional_charge": 5.0,
                "final_price": 115.0,
            }
        }
        mock_http_client.post.return_value = mock_response

        # Test OnDemand delivery
        price = price_module.calculate(1, 1, 12, 1.0, 1, 2)

        assert price.price == 120.0
        assert price.promo_discount == 10.0
        assert price.cod_enabled is False

    def test_calculate_different_item_types(self, price_module, mock_http_client):
        """Test price calculation with different item types."""
        mock_response = {
            "data": {
                "price": 40.0,
                "discount": 0.0,
                "promo_discount": 0.0,
                "plan_id": 3,
                "cod_enabled": True,
                "cod_percentage": 1.5,
                "additional_charge": 0.0,
                "final_price": 40.0,
            }
        }
        mock_http_client.post.return_value = mock_response

        # Test Document delivery
        price = price_module.calculate(1, 1, 48, 0.5, 1, 2)

        assert price.price == 40.0
        assert price.cod_percentage == 1.5

    def test_calculate_various_weights(self, price_module, mock_http_client):
        """Test price calculation with various weights."""
        mock_response = {
            "data": {
                "price": 150.0,
                "discount": 20.0,
                "promo_discount": 0.0,
                "plan_id": 4,
                "cod_enabled": True,
                "cod_percentage": 1.0,
                "additional_charge": 10.0,
                "final_price": 140.0,
            }
        }
        mock_http_client.post.return_value = mock_response

        # Test heavy parcel
        price = price_module.calculate(1, 2, 48, 5.0, 1, 2)

        assert price.price == 150.0
        assert price.additional_charge == 10.0

    def test_calculate_api_error(self, price_module, mock_http_client):
        """Test API error during price calculation."""
        mock_http_client.post.side_effect = APIError("Bad request", 400)

        with pytest.raises(APIError):
            price_module.calculate(1, 2, 48, 0.5, 1, 2)
