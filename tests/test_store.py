"""Tests for store management module."""

import pytest
from unittest.mock import Mock

from pathao.exceptions import ValidationError, NotFoundError, APIError
from pathao.models import Store, StoreList
from pathao.modules.store import StoreModule


class TestStoreModule:
    """Test cases for StoreModule."""

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
    def store_module(self, mock_http_client, mock_auth_module):
        """Store module instance."""
        return StoreModule(mock_http_client, mock_auth_module)

    def test_init(self, mock_http_client, mock_auth_module):
        """Test store module initialization."""
        module = StoreModule(mock_http_client, mock_auth_module)
        assert module.http_client == mock_http_client
        assert module.auth_module == mock_auth_module

    def test_create_success(self, store_module, mock_http_client, mock_auth_module):
        """Test successful store creation."""
        # Mock response
        mock_response = {
            "data": {
                "data": {
                    "store_id": 123,
                    "store_name": "Test Store",
                    "store_address": "123 Test Street, Dhaka",
                    "is_active": True,
                    "city_id": 1,
                    "zone_id": 2,
                    "hub_id": 3,
                    "is_default_store": False,
                    "is_default_return_store": False,
                }
            }
        }
        mock_http_client.post.return_value = mock_response

        # Call method
        store = store_module.create(
            store_name="Test Store",
            contact_name="John Doe",
            contact_number="01712345678",
            address="123 Test Street, Dhaka",
            city_id=1,
            zone_id=2,
            area_id=3,
        )

        # Verify
        assert isinstance(store, Store)
        assert store.store_id == 123
        assert store.store_name == "Test Store"
        assert store.is_active is True

        # Verify API call
        mock_auth_module.get_access_token.assert_called_once()
        mock_http_client.post.assert_called_once_with(
            "aladdin/api/v1/stores",
            {"Authorization": "Bearer test_token"},
            {
                "store_name": "Test Store",
                "contact_name": "John Doe",
                "contact_number": "01712345678",
                "address": "123 Test Street, Dhaka",
                "city_id": 1,
                "zone_id": 2,
                "area_id": 3,
            },
        )

    def test_create_validation_errors(self, store_module):
        """Test store creation validation errors."""
        # Test empty store name
        with pytest.raises(ValidationError) as exc_info:
            store_module.create("", "John", "01712345678", "123 Test St", 1, 2, 3)
        assert "name" in str(exc_info.value)

        # Test short store name
        with pytest.raises(ValidationError) as exc_info:
            store_module.create("AB", "John", "01712345678", "123 Test St", 1, 2, 3)
        assert "at least 3 characters" in str(exc_info.value)

        # Test long store name
        with pytest.raises(ValidationError) as exc_info:
            store_module.create("A" * 51, "John", "01712345678", "123 Test St", 1, 2, 3)
        assert "not exceed 50 characters" in str(exc_info.value)

        # Test invalid phone
        with pytest.raises(ValidationError) as exc_info:
            store_module.create("Test Store", "John", "123", "123 Test St", 1, 2, 3)
        assert "exactly 11 digits" in str(exc_info.value)

        # Test short address
        with pytest.raises(ValidationError) as exc_info:
            store_module.create("Test Store", "John", "01712345678", "Short", 1, 2, 3)
        assert "at least 15 characters" in str(exc_info.value)

        # Test invalid city_id
        with pytest.raises(ValueError) as exc_info:
            store_module.create(
                "Test Store", "John", "01712345678", "123 Test Street", 0, 2, 3
            )
        assert "city_id must be a positive integer" in str(exc_info.value)

    def test_list_success(self, store_module, mock_http_client, mock_auth_module):
        """Test successful store listing."""
        # Mock response
        mock_response = {
            "data": {
                "data": [
                    {
                        "store_id": 1,
                        "store_name": "Store 1",
                        "store_address": "Address 1",
                        "is_active": True,
                        "city_id": 1,
                        "zone_id": 2,
                        "hub_id": 3,
                        "is_default_store": True,
                        "is_default_return_store": False,
                    },
                    {
                        "store_id": 2,
                        "store_name": "Store 2",
                        "store_address": "Address 2",
                        "is_active": False,
                        "city_id": 2,
                        "zone_id": 3,
                        "hub_id": 4,
                        "is_default_store": False,
                        "is_default_return_store": True,
                    },
                ],
                "total": 2,
                "current_page": 1,
                "per_page": 10,
                "last_page": 1,
            }
        }
        mock_http_client.get.return_value = mock_response

        # Call method
        store_list = store_module.list(page=1, per_page=10)

        # Verify
        assert isinstance(store_list, StoreList)
        assert len(store_list.data) == 2
        assert store_list.total == 2
        assert store_list.current_page == 1

        # Verify first store
        store1 = store_list.data[0]
        assert store1.store_id == 1
        assert store1.store_name == "Store 1"
        assert store1.is_default_store is True

        # Verify API call
        mock_auth_module.get_access_token.assert_called_once()
        mock_http_client.get.assert_called_once_with(
            "aladdin/api/v1/stores",
            {"Authorization": "Bearer test_token"},
            {"page": 1, "per_page": 10},
        )

    def test_list_default_params(self, store_module, mock_http_client):
        """Test store listing with default parameters."""
        mock_http_client.get.return_value = {
            "data": {
                "data": [],
                "total": 0,
                "current_page": 1,
                "per_page": 10,
                "last_page": 1,
            }
        }

        store_module.list()

        mock_http_client.get.assert_called_once_with(
            "aladdin/api/v1/stores",
            {"Authorization": "Bearer test_token"},
            {"page": 1, "per_page": 10},
        )

    def test_list_validation_errors(self, store_module):
        """Test store listing validation errors."""
        # Test invalid page
        with pytest.raises(ValueError) as exc_info:
            store_module.list(page=0)
        assert "page must be a positive integer" in str(exc_info.value)

        # Test invalid per_page
        with pytest.raises(ValueError) as exc_info:
            store_module.list(per_page=0)
        assert "per_page must be between 1 and 100" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            store_module.list(per_page=101)
        assert "per_page must be between 1 and 100" in str(exc_info.value)

    def test_get_success(self, store_module, mock_http_client, mock_auth_module):
        """Test successful store retrieval."""
        # Mock response
        mock_response = {
            "data": {
                "store_id": 123,
                "store_name": "Test Store",
                "store_address": "123 Test Street",
                "is_active": True,
                "city_id": 1,
                "zone_id": 2,
                "hub_id": 3,
                "is_default_store": False,
                "is_default_return_store": True,
            }
        }
        mock_http_client.get.return_value = mock_response

        # Call method
        store = store_module.get(123)

        # Verify
        assert isinstance(store, Store)
        assert store.store_id == 123
        assert store.store_name == "Test Store"
        assert store.is_default_return_store is True

        # Verify API call
        mock_auth_module.get_access_token.assert_called_once()
        mock_http_client.get.assert_called_once_with(
            "aladdin/api/v1/stores/123", {"Authorization": "Bearer test_token"}
        )

    def test_get_validation_error(self, store_module):
        """Test store get validation error."""
        with pytest.raises(ValueError) as exc_info:
            store_module.get(0)
        assert "store_id must be a positive integer" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            store_module.get(-1)
        assert "store_id must be a positive integer" in str(exc_info.value)

    def test_get_not_found(self, store_module, mock_http_client):
        """Test store not found error."""
        mock_http_client.get.side_effect = Exception("404 Not Found")

        with pytest.raises(NotFoundError) as exc_info:
            store_module.get(999)
        assert "Store with identifier '999' not found" in str(exc_info.value)

    def test_get_api_error(self, store_module, mock_http_client):
        """Test API error during store retrieval."""
        mock_http_client.get.side_effect = APIError("Server error", 500)

        with pytest.raises(APIError):
            store_module.get(123)

    def test_create_api_error(self, store_module, mock_http_client):
        """Test API error during store creation."""
        mock_http_client.post.side_effect = APIError("Bad request", 400)

        with pytest.raises(APIError):
            store_module.create(
                "Test Store", "John", "01712345678", "123 Test Street", 1, 2, 3
            )

    def test_list_api_error(self, store_module, mock_http_client):
        """Test API error during store listing."""
        mock_http_client.get.side_effect = APIError("Server error", 500)

        with pytest.raises(APIError):
            store_module.list()
