"""Tests for location services module."""

import pytest
from unittest.mock import Mock

from pathao.exceptions import NotFoundError, APIError
from pathao.models import City, CityList, ZoneList, AreaList
from pathao.modules.location import LocationModule


class TestLocationModule:
    """Test cases for LocationModule."""

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
    def location_module(self, mock_http_client, mock_auth_module):
        """Location module instance."""
        return LocationModule(mock_http_client, mock_auth_module)

    def test_init(self, mock_http_client, mock_auth_module):
        """Test location module initialization."""
        module = LocationModule(mock_http_client, mock_auth_module)
        assert module.http_client == mock_http_client
        assert module.auth_module == mock_auth_module

    def test_get_cities_success(
        self, location_module, mock_http_client, mock_auth_module
    ):
        """Test successful cities retrieval."""
        mock_response = {
            "data": {
                "data": [
                    {"city_id": 1, "city_name": "Dhaka"},
                    {"city_id": 2, "city_name": "Chittagong"},
                ]
            }
        }
        mock_http_client.get.return_value = mock_response

        cities = location_module.get_cities()

        assert isinstance(cities, CityList)
        assert len(cities.data) == 2
        assert cities.data[0].city_id == 1
        assert cities.data[0].city_name == "Dhaka"
        assert cities.data[1].city_id == 2
        assert cities.data[1].city_name == "Chittagong"

        mock_auth_module.get_access_token.assert_called_once()
        mock_http_client.get.assert_called_once_with(
            "aladdin/api/v1/cities", {"Authorization": "Bearer test_token"}
        )

    def test_get_zones_success(
        self, location_module, mock_http_client, mock_auth_module
    ):
        """Test successful zones retrieval."""
        mock_response = {
            "data": {
                "data": [
                    {"zone_id": 1, "zone_name": "Dhanmondi"},
                    {"zone_id": 2, "zone_name": "Gulshan"},
                ]
            }
        }
        mock_http_client.get.return_value = mock_response

        zones = location_module.get_zones(1)

        assert isinstance(zones, ZoneList)
        assert len(zones.data) == 2
        assert zones.data[0].zone_id == 1
        assert zones.data[0].zone_name == "Dhanmondi"

        mock_auth_module.get_access_token.assert_called_once()
        mock_http_client.get.assert_called_once_with(
            "aladdin/api/v1/cities/1/zone-list", {"Authorization": "Bearer test_token"}
        )

    def test_get_zones_validation_error(self, location_module):
        """Test zones validation error."""
        with pytest.raises(ValueError) as exc_info:
            location_module.get_zones(0)
        assert "city_id must be a positive integer" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            location_module.get_zones(-1)
        assert "city_id must be a positive integer" in str(exc_info.value)

    def test_get_zones_not_found(self, location_module, mock_http_client):
        """Test zones not found error."""
        mock_http_client.get.side_effect = Exception("404 Not Found")

        with pytest.raises(NotFoundError) as exc_info:
            location_module.get_zones(999)
        assert "City with identifier '999' not found" in str(exc_info.value)

    def test_get_areas_success(
        self, location_module, mock_http_client, mock_auth_module
    ):
        """Test successful areas retrieval."""
        mock_response = {
            "data": {
                "data": [
                    {
                        "area_id": 1,
                        "area_name": "Dhanmondi 27",
                        "home_delivery_available": True,
                        "pickup_available": True,
                    },
                    {
                        "area_id": 2,
                        "area_name": "Dhanmondi 32",
                        "home_delivery_available": False,
                        "pickup_available": True,
                    },
                ]
            }
        }
        mock_http_client.get.return_value = mock_response

        areas = location_module.get_areas(1)

        assert isinstance(areas, AreaList)
        assert len(areas.data) == 2
        assert areas.data[0].area_id == 1
        assert areas.data[0].area_name == "Dhanmondi 27"
        assert areas.data[0].home_delivery_available is True
        assert areas.data[1].home_delivery_available is False

        mock_auth_module.get_access_token.assert_called_once()
        mock_http_client.get.assert_called_once_with(
            "aladdin/api/v1/zones/1/area-list", {"Authorization": "Bearer test_token"}
        )

    def test_get_areas_validation_error(self, location_module):
        """Test areas validation error."""
        with pytest.raises(ValueError) as exc_info:
            location_module.get_areas(0)
        assert "zone_id must be a positive integer" in str(exc_info.value)

    def test_get_areas_not_found(self, location_module, mock_http_client):
        """Test areas not found error."""
        mock_http_client.get.side_effect = Exception("404 Not Found")

        with pytest.raises(NotFoundError) as exc_info:
            location_module.get_areas(999)
        assert "Zone with identifier '999' not found" in str(exc_info.value)

    def test_get_city_by_name_success(self, location_module, mock_http_client):
        """Test successful city search by name."""
        mock_response = {
            "data": {
                "data": [
                    {"city_id": 1, "city_name": "Dhaka"},
                    {"city_id": 2, "city_name": "Chittagong"},
                ]
            }
        }
        mock_http_client.get.return_value = mock_response

        city = location_module.get_city_by_name("dhaka")

        assert isinstance(city, City)
        assert city.city_id == 1
        assert city.city_name == "Dhaka"

    def test_get_city_by_name_case_insensitive(self, location_module, mock_http_client):
        """Test case-insensitive city search."""
        mock_response = {
            "data": {
                "data": [
                    {"city_id": 1, "city_name": "Dhaka"},
                ]
            }
        }
        mock_http_client.get.return_value = mock_response

        city = location_module.get_city_by_name("DHAKA")
        assert city.city_name == "Dhaka"

        city = location_module.get_city_by_name("dhaka")
        assert city.city_name == "Dhaka"

    def test_get_city_by_name_validation_error(self, location_module):
        """Test city search validation error."""
        with pytest.raises(ValueError) as exc_info:
            location_module.get_city_by_name("")
        assert "name is required" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            location_module.get_city_by_name(None)
        assert "name is required" in str(exc_info.value)

    def test_get_city_by_name_not_found(self, location_module, mock_http_client):
        """Test city not found by name."""
        mock_response = {
            "data": {
                "data": [
                    {"city_id": 1, "city_name": "Dhaka"},
                ]
            }
        }
        mock_http_client.get.return_value = mock_response

        with pytest.raises(NotFoundError) as exc_info:
            location_module.get_city_by_name("Sylhet")
        assert "City with identifier 'sylhet' not found" in str(exc_info.value)

    def test_get_cities_api_error(self, location_module, mock_http_client):
        """Test API error during cities retrieval."""
        mock_http_client.get.side_effect = APIError("Server error", 500)

        with pytest.raises(APIError):
            location_module.get_cities()

    def test_get_zones_api_error(self, location_module, mock_http_client):
        """Test API error during zones retrieval."""
        mock_http_client.get.side_effect = APIError("Server error", 500)

        with pytest.raises(APIError):
            location_module.get_zones(1)

    def test_get_areas_api_error(self, location_module, mock_http_client):
        """Test API error during areas retrieval."""
        mock_http_client.get.side_effect = APIError("Server error", 500)

        with pytest.raises(APIError):
            location_module.get_areas(1)
