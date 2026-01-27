"""Location services module for Pathao Python SDK."""

from typing import TYPE_CHECKING

from ..exceptions import NotFoundError
from ..models import City, CityList, Zone, ZoneList, Area, AreaList

if TYPE_CHECKING:
    from ..http_client import HTTPClient
    from .auth import AuthModule


class LocationModule:
    """Location services operations."""

    def __init__(self, http_client: "HTTPClient", auth_module: "AuthModule"):
        """Initialize location module."""
        self.http_client = http_client
        self.auth_module = auth_module

    def get_cities(self) -> CityList:
        """Get all cities."""
        token = self.auth_module.get_access_token()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.http_client.get("aladdin/api/v1/city-list", headers)

        # Handle different response structures
        if "data" in response and "data" in response["data"]:
            # Nested data structure
            city_data = response["data"]["data"]
        elif "data" in response:
            # Direct data structure
            city_data = response["data"]
        else:
            # Response is the data itself
            city_data = response

        cities = [
            City(city_id=city["city_id"], city_name=city["city_name"])
            for city in city_data
        ]

        return CityList(data=cities)

    def get_zones(self, city_id: int) -> ZoneList:
        """Get zones for a city."""
        if not isinstance(city_id, int) or city_id <= 0:
            raise ValueError("city_id must be a positive integer")

        token = self.auth_module.get_access_token()
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = self.http_client.get(
                f"aladdin/api/v1/cities/{city_id}/zone-list", headers
            )

            # Handle different response structures
            if "data" in response and "data" in response["data"]:
                zone_data = response["data"]["data"]
            elif "data" in response:
                zone_data = response["data"]
            else:
                zone_data = response

            zones = [
                Zone(zone_id=zone["zone_id"], zone_name=zone["zone_name"])
                for zone in zone_data
            ]

            return ZoneList(data=zones)
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                raise NotFoundError("City", str(city_id))
            raise

    def get_areas(self, zone_id: int) -> AreaList:
        """Get areas for a zone."""
        if not isinstance(zone_id, int) or zone_id <= 0:
            raise ValueError("zone_id must be a positive integer")

        token = self.auth_module.get_access_token()
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = self.http_client.get(
                f"aladdin/api/v1/zones/{zone_id}/area-list", headers
            )

            # Handle different response structures
            if "data" in response and "data" in response["data"]:
                area_data = response["data"]["data"]
            elif "data" in response:
                area_data = response["data"]
            else:
                area_data = response

            areas = [
                Area(
                    area_id=area["area_id"],
                    area_name=area["area_name"],
                    home_delivery_available=area["home_delivery_available"],
                    pickup_available=area["pickup_available"],
                )
                for area in area_data
            ]

            return AreaList(data=areas)
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                raise NotFoundError("Zone", str(zone_id))
            raise

    def get_city_by_name(self, name: str) -> City:
        """Find city by name (case-insensitive)."""
        if not name or not isinstance(name, str):
            raise ValueError("name is required and must be a string")

        name = name.strip().lower()
        if not name:
            raise ValueError("name cannot be empty")

        cities = self.get_cities()

        for city in cities.data:
            if city.city_name.lower() == name:
                return city

        raise NotFoundError("City", name)
