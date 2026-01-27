"""Store management module for Pathao Python SDK."""

from typing import TYPE_CHECKING

from ..exceptions import NotFoundError
from ..models import Store, StoreList
from ..validators import validate_name, validate_phone, validate_address

if TYPE_CHECKING:
    from ..http_client import HTTPClient
    from .auth import AuthModule


class StoreModule:
    """Store management operations."""

    def __init__(self, http_client: "HTTPClient", auth_module: "AuthModule"):
        """Initialize store module."""
        self.http_client = http_client
        self.auth_module = auth_module

    def create(
        self,
        store_name: str,
        contact_name: str,
        contact_number: str,
        address: str,
        city_id: int,
        zone_id: int,
        area_id: int,
    ) -> Store:
        """Create a new store."""
        # Validate inputs
        store_name = validate_name(store_name, min_length=3, max_length=50)
        contact_name = validate_name(contact_name, min_length=3, max_length=50)
        contact_number = validate_phone(contact_number, length=11)
        address = validate_address(address, min_length=15, max_length=120)

        # Validate location IDs
        if not isinstance(city_id, int) or city_id <= 0:
            raise ValueError("city_id must be a positive integer")
        if not isinstance(zone_id, int) or zone_id <= 0:
            raise ValueError("zone_id must be a positive integer")
        if not isinstance(area_id, int) or area_id <= 0:
            raise ValueError("area_id must be a positive integer")

        # Get access token
        token = self.auth_module.get_access_token()

        # Prepare request
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "store_name": store_name,
            "contact_name": contact_name,
            "contact_number": contact_number,
            "address": address,
            "city_id": city_id,
            "zone_id": zone_id,
            "area_id": area_id,
        }

        # Make API request
        response = self.http_client.post("aladdin/api/v1/stores", headers, data)

        # Parse response
        store_data = response["data"]["data"]
        return Store(
            store_id=store_data["store_id"],
            store_name=store_data["store_name"],
            store_address=store_data["store_address"],
            is_active=store_data["is_active"],
            city_id=store_data["city_id"],
            zone_id=store_data["zone_id"],
            hub_id=store_data["hub_id"],
            is_default_store=store_data["is_default_store"],
            is_default_return_store=store_data["is_default_return_store"],
        )

    def list(self, page: int = 1, per_page: int = 10) -> StoreList:
        """List stores with pagination."""
        # Validate pagination params
        if not isinstance(page, int) or page < 1:
            raise ValueError("page must be a positive integer")
        if not isinstance(per_page, int) or per_page < 1 or per_page > 100:
            raise ValueError("per_page must be between 1 and 100")

        # Get access token
        token = self.auth_module.get_access_token()

        # Prepare request
        headers = {"Authorization": f"Bearer {token}"}
        params = {"page": page, "per_page": per_page}

        # Make API request
        response = self.http_client.get("aladdin/api/v1/stores", headers, params)

        # Parse response
        data = response["data"]
        stores = [
            Store(
                store_id=store["store_id"],
                store_name=store["store_name"],
                store_address=store["store_address"],
                is_active=store["is_active"],
                city_id=store["city_id"],
                zone_id=store["zone_id"],
                hub_id=store["hub_id"],
                is_default_store=store["is_default_store"],
                is_default_return_store=store["is_default_return_store"],
            )
            for store in data["data"]
        ]

        return StoreList(
            data=stores,
            total=data["total"],
            current_page=data["current_page"],
            per_page=data["per_page"],
            last_page=data["last_page"],
        )

    def get(self, store_id: int) -> Store:
        """Get a specific store by ID."""
        # Validate store_id
        if not isinstance(store_id, int) or store_id <= 0:
            raise ValueError("store_id must be a positive integer")

        # Get access token
        token = self.auth_module.get_access_token()

        # Prepare request
        headers = {"Authorization": f"Bearer {token}"}

        try:
            # Make API request
            response = self.http_client.get(
                f"aladdin/api/v1/stores/{store_id}", headers
            )

            # Parse response
            store_data = response["data"]
            return Store(
                store_id=store_data["store_id"],
                store_name=store_data["store_name"],
                store_address=store_data["store_address"],
                is_active=store_data["is_active"],
                city_id=store_data["city_id"],
                zone_id=store_data["zone_id"],
                hub_id=store_data["hub_id"],
                is_default_store=store_data["is_default_store"],
                is_default_return_store=store_data["is_default_return_store"],
            )
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                raise NotFoundError("Store", str(store_id))
            raise
