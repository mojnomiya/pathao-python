"""Pytest configuration and shared fixtures for Pathao Python SDK tests."""

import pytest
from unittest.mock import Mock
from pathao.http_client import HTTPClient
from pathao.modules.auth import AuthModule
from pathao.models import AuthToken


@pytest.fixture
def mock_http_client():
    """Mock HTTP client for testing."""
    client = Mock(spec=HTTPClient)
    client.get.return_value = {"status": "success"}
    client.post.return_value = {"status": "success"}
    return client


@pytest.fixture
def mock_auth_module():
    """Mock authentication module for testing."""
    auth = Mock(spec=AuthModule)
    auth.get_access_token.return_value = "mock_access_token"
    auth.is_token_valid.return_value = True
    auth.refresh_token.return_value = None
    return auth


@pytest.fixture
def sample_store_data():
    """Sample store data for testing."""
    return {
        "data": {
            "store_id": 1,
            "name": "Test Store",
            "contact_name": "John Doe",
            "contact_number": "01712345678",
            "address": "123 Test Street, Dhaka",
            "secondary_contact": "01987654321",
            "hub_id": 1,
        }
    }


@pytest.fixture
def sample_order_data():
    """Sample order data for testing."""
    return {
        "data": {
            "consignment_id": "D-12345",
            "order_status": "Pending",
            "item_description": "Test Item",
            "amount_to_collect": 100.0,
            "recipient_name": "Jane Doe",
            "recipient_phone": "01712345678",
            "recipient_address": "456 Test Road, Dhaka",
        }
    }


@pytest.fixture
def sample_location_data():
    """Sample location data for testing."""
    return {
        "data": {
            "cities": [
                {"city_id": 1, "city_name": "Dhaka"},
                {"city_id": 2, "city_name": "Chittagong"},
            ],
            "zones": [
                {"zone_id": 1, "zone_name": "Dhanmondi", "city_id": 1},
                {"zone_id": 2, "zone_name": "Gulshan", "city_id": 1},
            ],
            "areas": [
                {"area_id": 1, "area_name": "Dhanmondi 27", "zone_id": 1},
                {"area_id": 2, "area_name": "Gulshan 1", "zone_id": 2},
            ],
        }
    }


@pytest.fixture
def sample_price_data():
    """Sample price data for testing."""
    return {
        "data": {
            "price": 60.0,
            "discount": 5.0,
            "promo_discount": 0.0,
            "cod_enabled": True,
            "cod_percentage": 1.0,
            "additional_charges": 0.0,
            "final_price": 55.0,
            "plan_id": 1,
        }
    }


@pytest.fixture
def sample_auth_token():
    """Sample auth token for testing."""
    return AuthToken(
        access_token="mock_access_token",
        refresh_token="mock_refresh_token",
        expires_in=3600,
        token_type="Bearer",
    )
